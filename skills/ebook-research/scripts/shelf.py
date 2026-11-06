#!/usr/bin/env python3
"""
shelf.py — query a local Recoll index of an ebook library, and drill into hits.

Design rule: every subcommand prints BOUNDED output. Full extracted text always
goes to a cache file on disk; only a slice comes back to the caller. A single
large PDF dumps ~600KB of text, which is why nothing here streams raw content.

Subcommands:
  search  QUERY                 rank BOOKS (not fragments) matching a query
  hits    BOOK QUERY            locate where in one book the query lands
  read    BOOK                  extract real prose at a location
  info    BOOK                  metadata, page count / chapter list
  status                        index health and freshness
"""

import argparse
import base64
import html
import os
import re
import shutil
import subprocess
import sys
import zipfile
from html.parser import HTMLParser

CACHE = os.path.expanduser("~/.cache/ebook-research")
APP = "/Applications/Recoll.app/Contents/MacOS"


# ---------------------------------------------------------------- binaries

def _bin(name):
    """Recoll ships its CLI inside the .app bundle on macOS; PATH first."""
    found = shutil.which(name)
    if found:
        return found
    local = os.path.join(APP, name)
    if os.path.exists(local):
        return local
    return None


def _need(name):
    b = _bin(name)
    if not b:
        sys.exit(f"error: {name} not found (looked in PATH and {APP})")
    return b


def _run(cmd):
    """Run a command, discard stderr (recoll is chatty about config paths)."""
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout.decode("utf-8", "replace")


# ---------------------------------------------------------------- recoll

FIELDS = ["url", "ipath", "title", "author", "filename",
          "pcbytes", "relevancyrating", "mtype", "abstract"]


def rq_records(query, count, first=0):
    """Structured results via -F base64 — immune to spaces/brackets in paths."""
    out = _run([_need("recollq"), "-n", f"{first}-{count}",
                "-F", " ".join(FIELDS), query])
    recs = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split(" ")
        if len(parts) < len(FIELDS):
            continue
        rec = {}
        for k, v in zip(FIELDS, parts):
            try:
                rec[k] = base64.b64decode(v).decode("utf-8", "replace") if v else ""
            except Exception:
                rec[k] = ""
        if rec.get("url"):
            recs.append(rec)
    return recs


RESULT_LINE = re.compile(r"^\S+/\S*\t\[")


def rq_snippets(query, count, per=3, first=0):
    """
    Page-numbered snippets via -A -p. Returned as a list aligned by result
    index with rq_records() for the same query+slice (recoll ordering is
    deterministic). Missing blocks stay aligned because result boundaries are
    detected independently of the snippet blocks.
    """
    out = _run([_need("recollq"), "-n", f"{first}-{count}",
                "-A", "-p", str(per), query])
    blocks, cur, in_snips = [], None, False
    for line in out.splitlines():
        if RESULT_LINE.match(line):
            if cur is not None:
                blocks.append(cur)
            cur, in_snips = [], False
            continue
        if cur is None:
            continue
        if line.strip() == "SNIPPETS":
            in_snips = True
            continue
        if line.strip() == "/SNIPPETS":
            in_snips = False
            continue
        if in_snips:
            m = re.match(r"^(\d+)\s*:\s*(.*)$", line)
            if m:
                cur.append((int(m.group(1)), m.group(2).strip()))
    if cur is not None:
        blocks.append(cur)
    return blocks


def path_of(rec):
    u = rec.get("url", "")
    return u[7:] if u.startswith("file://") else u


def book_label(rec):
    p = path_of(rec)
    base = os.path.basename(p)
    t = (rec.get("title") or "").strip()
    stem = os.path.splitext(base)[0]
    # subdoc titles are chapter names; prefer the filename stem as book identity
    if t and len(t) > 3 and t.lower() not in ("index", "cover", "contents"):
        if len(stem) > 60:
            return t
    return stem


def clip(s, n):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


GENERIC = {"index", "cover", "contents", "untitled", "text", "toc", "titlepage"}


def index_like(text):
    """
    Back-of-book indexes and tables of contents match almost any query
    ("45 in math-skills acquisition, 79-81") and would otherwise crowd out
    real prose. Detect them by density of page-number tokens.
    """
    toks = (text or "").split()
    if len(toks) < 6:
        return False
    numeric = sum(1 for t in toks if re.search(r"\d", t))
    if numeric / len(toks) > 0.22:
        return True
    # page-range runs ("79-81", "108-13") are near-proof of an index
    return len(re.findall(r"\b\d+[–—-]\d+\b", text)) >= 2


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def dedupe_editions(ranked):
    """
    The library keeps the same book in several year folders, often under
    slightly different filenames. Collapse those so one book occupies one slot:
    a title is a duplicate when its normalized form is a prefix of (or
    contained in) one already kept. The 20-char floor keeps short generic
    titles from swallowing unrelated books.
    """
    kept, seen = [], []
    for b in ranked:
        n = _norm(book_label(b["rec"]))
        dup = next((k for k in seen
                    if len(n) >= 20 and len(k) >= 20 and (n in k or k in n)), None)
        if dup is not None:
            for prev in kept:
                if _norm(book_label(prev["rec"])) == dup:
                    prev.setdefault("copies", []).append(path_of(b["rec"]))
                    prev["n"] += b["n"]
                    break
            continue
        seen.append(n)
        kept.append(b)
    return kept


# ---------------------------------------------------------------- search

def cmd_search(a):
    q = a.query
    if a.ext:
        q = f"ext:{a.ext} {q}"
    if a.dir:
        q = f'dir:"{a.dir}" {q}'

    depth = max(a.books * 6, 40)
    recs = rq_records(q, depth)
    if not recs:
        print(f"No results for: {q}")
        print("Try: broader terms, drop quotes, or check `shelf.py status`.")
        return

    snips = rq_snippets(q, depth, per=a.snips)
    aligned = len(snips) == len(recs)

    books = {}
    for i, r in enumerate(recs):
        p = path_of(r)
        b = books.setdefault(p, {"rec": r, "n": 0, "snips": [], "rel": 0})
        b["n"] += 1
        rel = int(re.sub(r"\D", "", r.get("relevancyrating") or "0") or 0)
        b["rel"] = max(b["rel"], rel)
        if aligned:
            for page, text in snips[i]:
                b["snips"].append((page, text, r.get("ipath", "")))
        elif r.get("abstract"):
            b["snips"].append((0, r["abstract"], r.get("ipath", "")))

    # a book whose every snippet is an index/TOC entry is not really about the
    # topic — keep it, but behind books with real prose
    for b in books.values():
        prose = [s for s in b["snips"] if not index_like(s[1])]
        b["prose_only"] = bool(prose)
        if prose:
            b["snips"] = prose

    ranked = sorted(books.values(),
                    key=lambda b: (not b["prose_only"], -b["rel"], -b["n"]))
    if not a.no_dedupe:
        ranked = dedupe_editions(ranked)
    ranked = ranked[: a.books]

    print(f"query: {q}")
    print(f"{len(books)} books matched (showing {len(ranked)})\n")
    for i, b in enumerate(ranked, 1):
        r, p = b["rec"], path_of(b["rec"])
        ext = os.path.splitext(p)[1].lstrip(".").lower()
        author = clip(r.get("author", ""), 40)
        head = f"[{i}] {clip(book_label(r), 70)}"
        if author:
            head += f" — {author}"
        print(head)
        print(f"    {ext}, {b['n']} hit(s), rel {b['rel']}%")
        print(f"    {p}")
        if b.get("copies"):
            print(f"    ({len(b['copies'])} duplicate cop(ies) elsewhere in the library)")
        seen = set()
        for page, text, ipath in b["snips"][: a.snips]:
            t = clip(text, 160)
            if not t or t in seen:
                continue
            seen.add(t)
            loc = f"p.{page}" if page else (ipath.split("/")[-1] if ipath else "—")
            print(f"    · {loc} | {t}")
        print()

    print("next: shelf.py hits <book> \"<query>\"   → where in that book")
    print("      shelf.py read <book> --page N     → the actual prose")


# ---------------------------------------------------------------- hits

def cmd_hits(a):
    book = os.path.abspath(os.path.expanduser(a.book))
    if not os.path.exists(book):
        sys.exit(f"error: no such file: {book}")
    parent = os.path.dirname(book)

    # filename: is unreliable for hyphenated names, and subdocs don't carry it.
    # dir: restriction + exact path match is exact and always works.
    q = f'dir:"{parent}" {a.query}'
    recs = rq_records(q, 0)
    snips = rq_snippets(q, 0, per=a.snips)
    aligned = len(snips) == len(recs)

    rows = []
    for i, r in enumerate(recs):
        if path_of(r) != book:
            continue
        s = snips[i] if aligned else [(0, r.get("abstract", ""))]
        rows.append((r, s))

    if not rows:
        print(f"No hits for '{a.query}' in {os.path.basename(book)}")
        print("The book may match on other terms — try `shelf.py info` for its structure.")
        return

    is_pdf = book.lower().endswith(".pdf")
    print(f"{os.path.basename(book)}")
    print(f"{len(rows)} matching section(s) for: {a.query}\n")
    for r, s in rows[: a.max]:
        ipath = r.get("ipath", "")
        title = clip(r.get("title", ""), 60)
        # many epubs title every section "index"; the chapter file is more useful
        if not title or title.lower() in GENERIC:
            title = ipath.split("/")[-1] if ipath else "—"
        pages = sorted({p for p, _ in s if p})
        if is_pdf and pages:
            loc = "--page " + " --page ".join(str(p) for p in pages[:4])
        elif ipath:
            loc = f'--ipath "{ipath}"'
        else:
            loc = "(whole file)"
        print(f"· {title}")
        print(f"  read with: {loc}")
        for p, t in s[: a.snips]:
            print(f"    {('p.' + str(p)) if p else '  '} {clip(t, 150)}")
        print()
    if len(rows) > a.max:
        print(f"... {len(rows) - a.max} more (use --max)")


# ---------------------------------------------------------------- read

class Stripper(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head"):
            self.skip += 1
        elif tag in ("p", "div", "br", "h1", "h2", "h3", "h4", "li"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head") and self.skip:
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)

    def text(self):
        t = html.unescape("".join(self.out))
        t = re.sub(r"[ \t\xa0]+", " ", t)
        t = re.sub(r"\n\s*\n\s*\n+", "\n\n", t)
        return "\n".join(ln.strip() for ln in t.splitlines()).strip()


def zip_entry(book, ipath):
    """epub ipath is a zip entry; recoll may report it without its dir prefix."""
    with zipfile.ZipFile(book) as z:
        names = z.namelist()
        if ipath in names:
            return z.read(ipath)
        base = ipath.split("/")[-1].lower()
        for n in names:
            if n.split("/")[-1].lower() == base:
                return z.read(n)
    return None


def extract(book, page=None, window=2, ipath=None):
    """Return (text, description-of-what-was-extracted)."""
    ext = os.path.splitext(book)[1].lower()

    if ext == ".pdf":
        pt = _need("pdftotext")
        if page:
            first, last = max(1, page - window), page + window
            txt = _run([pt, "-f", str(first), "-l", str(last), book, "-"])
            return txt, f"pages {first}-{last}"
        return _run([pt, book, "-"]), "whole PDF"

    if ext in (".epub", ".htmlz", ".zip"):
        if not ipath:
            return None, "epub needs --ipath (see `shelf.py info` or `hits`)"
        raw = zip_entry(book, ipath)
        if raw is None:
            return None, f"no zip entry matching '{ipath}'"
        s = Stripper()
        s.feed(raw.decode("utf-8", "replace"))
        return s.text(), f"chapter {ipath}"

    if ext in (".txt", ".md", ".htm", ".html"):
        raw = open(book, "rb").read().decode("utf-8", "replace")
        if ext in (".htm", ".html"):
            s = Stripper()
            s.feed(raw)
            return s.text(), "whole file"
        return raw, "whole file"

    # mobi/azw3/doc etc: fall back to recoll's own extracted text
    name = os.path.basename(book)
    txt = _run([_need("recollq"), "-n", "1", "-d", f'filename:"{name}"'])
    txt = re.sub(r"^.*?/SNIPPETS", "", txt, flags=re.S)
    return txt, "recoll-extracted text"


def cmd_read(a):
    book = os.path.abspath(os.path.expanduser(a.book))
    if not os.path.exists(book):
        sys.exit(f"error: no such file: {book}")

    text, what = extract(book, a.page, a.window, a.ipath)
    if not text:
        sys.exit(f"error: {what}")

    os.makedirs(CACHE, exist_ok=True)
    slug = re.sub(r"[^A-Za-z0-9]+", "-", os.path.basename(book))[:60]
    tag = f"p{a.page}" if a.page else (re.sub(r"[^A-Za-z0-9]+", "-", a.ipath or "full")[:30])
    out = a.out or os.path.join(CACHE, f"{slug}--{tag}.txt")
    with open(out, "w") as f:
        f.write(text)

    words = len(text.split())
    print(f"{os.path.basename(book)} — {what}")
    print(f"{words} words, {len(text)} chars → full text saved to:\n{out}\n")

    if a.grep:
        pat = re.compile(a.grep, re.I)
        shown = 0
        for m in pat.finditer(text):
            s, e = max(0, m.start() - a.chars // 2), m.end() + a.chars // 2
            print("---")
            print(text[s:e].strip())
            shown += 1
            if shown >= a.matches:
                break
        if not shown:
            print(f"(no match for /{a.grep}/ — showing opening instead)\n")
            print(text[: a.chars])
        else:
            print(f"\n--- {shown} passage(s) shown; read {out} for the rest")
        return

    print(text[: a.chars])
    if len(text) > a.chars:
        print(f"\n--- truncated at {a.chars} chars. Read {out} for the full text "
              f"(use Read with offset/limit, or --grep to jump to a term).")


# ---------------------------------------------------------------- info

def cmd_info(a):
    book = os.path.abspath(os.path.expanduser(a.book))
    if not os.path.exists(book):
        sys.exit(f"error: no such file: {book}")
    ext = os.path.splitext(book)[1].lower()
    size = os.path.getsize(book)
    print(f"{os.path.basename(book)}")
    print(f"{book}")
    print(f"{size / 1024 / 1024:.1f} MB\n")

    if ext == ".pdf":
        info = _run([_need("pdfinfo"), book])
        for ln in info.splitlines():
            if re.match(r"^(Title|Author|Pages|CreationDate|Subject|Keywords)", ln):
                print(ln.strip())
        return

    if ext in (".epub", ".htmlz", ".zip"):
        with zipfile.ZipFile(book) as z:
            docs = [(i.filename, i.file_size) for i in z.infolist()
                    if re.search(r"\.x?html?$", i.filename, re.I)]
        docs.sort(key=lambda d: d[0])
        print(f"{len(docs)} content documents (--ipath values):")
        for name, sz in docs[: a.max]:
            print(f"  {sz:>8}  {name}")
        if len(docs) > a.max:
            print(f"  ... {len(docs) - a.max} more (use --max)")
        return

    print(f"(no structural reader for {ext}; `read` will use recoll's text)")


# ---------------------------------------------------------------- status

def cmd_status(a):
    conf = os.path.expanduser("~/.recoll")
    db = os.path.join(conf, "xapiandb")
    print(f"recollq:  {_bin('recollq') or 'NOT FOUND'}")
    print(f"pdftotext:{_bin('pdftotext') or 'NOT FOUND'}")
    print(f"index:    {db}")
    if not os.path.isdir(db):
        print("  -> no index. Build one: recollindex")
        return

    import time
    mt = os.path.getmtime(db)
    age_h = (time.time() - mt) / 3600
    print(f"  updated: {time.strftime('%Y-%m-%d %H:%M', time.localtime(mt))} "
          f"({age_h:.0f}h ago)")

    st = os.path.join(conf, "idxstatus.txt")
    if os.path.exists(st):
        kv = dict(re.findall(r"^(\w+)\s*=\s*(.*)$", open(st).read(), re.M))
        print(f"  docs:    {kv.get('dbtotdocs', '?')} "
              f"(from {kv.get('totfiles', '?')} files)")

    cf = os.path.join(conf, "recoll.conf")
    if os.path.exists(cf):
        for m in re.finditer(r"^topdirs\s*=\s*(.*)$", open(cf).read(), re.M):
            print(f"  indexes: {m.group(1)}")
            for d in re.findall(r'"[^"]+"|\S+', m.group(1)):
                d = os.path.expanduser(d.strip('"'))
                if os.path.isdir(d):
                    stale = subprocess.run(
                        ["find", d, "-type", "f", "-newer", db],
                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                    n = len(stale.stdout.decode().splitlines())
                    print(f"    {d}: {n} file(s) newer than index")

    print("\nNo daemon needed — queries read the index directly off disk.")
    print("Refresh after adding books:  recollindex   (or nice recollindex &)")


# ---------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="rank books matching a query")
    s.add_argument("query")
    s.add_argument("--books", type=int, default=8, help="books to show (default 8)")
    s.add_argument("--snips", type=int, default=3, help="snippets per book")
    s.add_argument("--ext", help="epub | pdf | mobi | txt")
    s.add_argument("--dir", help="restrict to a folder path")
    s.add_argument("--no-dedupe", action="store_true",
                   help="show duplicate editions as separate results")
    s.set_defaults(func=cmd_search)

    h = sub.add_parser("hits", help="locate a query inside one book")
    h.add_argument("book")
    h.add_argument("query")
    h.add_argument("--max", type=int, default=12)
    h.add_argument("--snips", type=int, default=2)
    h.set_defaults(func=cmd_hits)

    r = sub.add_parser("read", help="extract real prose at a location")
    r.add_argument("book")
    r.add_argument("--page", type=int, help="PDF page number")
    r.add_argument("--window", type=int, default=2, help="pages either side (default 2)")
    r.add_argument("--ipath", help="epub chapter (zip entry)")
    r.add_argument("--grep", help="show passages around this term instead of the opening")
    r.add_argument("--matches", type=int, default=3, help="max --grep passages")
    r.add_argument("--chars", type=int, default=4000, help="chars to print (default 4000)")
    r.add_argument("--out", help="write full text here instead of the cache")
    r.set_defaults(func=cmd_read)

    i = sub.add_parser("info", help="metadata / chapter list")
    i.add_argument("book")
    i.add_argument("--max", type=int, default=40)
    i.set_defaults(func=cmd_info)

    st = sub.add_parser("status", help="index health")
    st.set_defaults(func=cmd_status)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
