---
name: ebook-research
description: Research a topic against a personal ebook library (PDF/EPUB) indexed locally with Recoll — finds which books cover a subject, locates the exact chapter or page, and pulls the real prose for quoting with citations. Use for evergreen, conceptual, or foundational research where web articles stay surface-level: philosophy, craft, history, psychology, business principles, writing technique, science fundamentals, "the theory behind X". Trigger — "what do my books say about", "check my library", "search my ebooks", "any books on", "go deeper than the web on this", "find a source/quote for this claim", "back this up with a real source", or whenever a research task needs depth rather than the latest news. NOT for current events, breaking releases, or fast-moving tech (AI models, framework versions, news) — use web search for those.
---

<essential_principles>

## What this is for

The library is the user's own ebook collection, indexed by Recoll. If you don't know where it lives, run `python3 scripts/shelf.py status` (it lists the indexed folders) or ask. Books are the
right source when a topic is **settled, deep, or conceptual** — a real author spent
300 pages on what a blog post covers in 800 words. The web is the right source when
a topic is **current** — releases, model launches, versions, news.

Split a research task accordingly. Most real questions want both: the web for what
changed this month, books for the underlying principle. Say which source each claim
came from.

## Non-negotiable: bounded output

A single large PDF holds ~600KB of extracted text. Dumping one into context can end
a session. Therefore:

- **Never** `cat`, `pdftotext`, or `recollq -d` a book straight into context.
- **Always** go through `scripts/shelf.py`. Every subcommand caps what it prints and
  writes full extractions to `~/.cache/ebook-research/`.
- To read more of a cached extraction, use the Read tool with `offset`/`limit`, or
  re-run `read --grep TERM`. Never read a whole cache file blind.

</essential_principles>

## Setup facts

- **Prerequisite: Recoll** (https://www.recoll.org). If `recollq` is not on PATH (and, on macOS, `/Applications/Recoll.app` is missing), stop and tell the user to install it: on Linux use the package manager (`apt install recoll`, etc.); on macOS install the official DMG from https://www.recoll.org/pages/recoll-macos.html and drag it to `/Applications` (it is unsigned, so on Apple Silicon also run `xattr -rd com.apple.quarantine /Applications/Recoll.app`). A fresh install has no index — `shelf.py status` will show 0 docs until `recollindex` has run over the user's ebook folder (set in Recoll's indexing configuration; slow, so the user runs it). `shelf.py` itself is stdlib-only Python.
- `recollq`, `pdftotext` and `pdfinfo` are found automatically: PATH first, then the macOS app bundle (`/Applications/Recoll.app/Contents/MacOS/`).
- **No application needs to be running.** `recollq` reads the Xapian index directly
  off disk. Recoll.app is only the GUI; never launch it to run a search.
- Run `python3 scripts/shelf.py status` if anything looks wrong — it reports the
  index date, doc count, indexed folders, and how many files are newer than the
  index.
- After adding books, the index needs a manual refresh (no live monitor):
  `recollindex` (inside the app bundle on macOS). It is slow — suggest the
  user run it themselves with `! nice recollindex` rather than blocking a session.

## The four-level ladder

Never stop at level 1. Snippets are ~40-character fragments — enough to rank books,
useless as evidence. Real research means descending to level 3.

### Level 1 — Which books cover this

```bash
python3 scripts/shelf.py search "QUERY" --books 8
```

Ranks **books**, not fragments, collapsing the duplicate editions scattered across
year folders. Returns title, author, format, hit count, path, and locator snippets.

Useful flags: `--ext epub|pdf`, `--dir /path/to/subfolder`, `--snips N`,
`--no-dedupe`.

### Level 2 — Where inside the book

```bash
python3 scripts/shelf.py hits "/path/to/book.epub" "QUERY" --max 12
```

Lists every matching section with a ready-to-paste locator — `--page N` for PDFs,
`--ipath "chapter.xhtml"` for EPUBs. This is how you find the chapter that actually
argues the point instead of the one that mentions the term in passing.

`info` shows a book's structure when a query is too vague to locate:

```bash
python3 scripts/shelf.py info "/path/to/book.pdf"     # title, author, page count
python3 scripts/shelf.py info "/path/to/book.epub"    # chapter list (--ipath values)
```

### Level 3 — Read the actual prose

```bash
# PDF: a page window (default ±2 pages)
python3 scripts/shelf.py read "/path/book.pdf" --page 42 --window 2

# EPUB: one chapter
python3 scripts/shelf.py read "/path/book.epub" --ipath "Section0004.xhtml"

# Jump straight to the passages that matter inside a long chapter
python3 scripts/shelf.py read "/path/book.epub" --ipath "ch07.xhtml" \
    --grep "negative visualization" --matches 3
```

`--grep` is the workhorse: it prints windows around each match instead of the
chapter opening. Default print cap is 4000 chars (`--chars`); the full text is
always cached to disk and the path is printed.

Formats: PDF via page ranges, EPUB/HTMLZ via zip chapter, TXT/HTML read directly,
MOBI/AZW3/DOC fall back to Recoll's own extracted text.

### Level 4 — Synthesize with citations

Books earn their keep through attribution. Every claim pulled from the library
carries a real citation:

> Irvine argues the Stoics practiced "negative visualization" as a form of
> preemptive gratitude rather than pessimism.
> — *A Guide to the Good Life*, William B. Irvine, ch. 4

Rules for synthesis:
- Quote from level-3 prose only. Never quote a level-1 snippet — fragments are
  truncated mid-sentence and will misquote the author.
- Cite book title, author, and locator (page for PDF, chapter for EPUB).
- When several books agree, say so, and note where they disagree — that
  disagreement is usually the interesting part, and it is exactly what a single
  web article cannot give you.
- Distinguish "this book asserts" from "this is established" — a book is one
  author's argument, not a fact-check.

## Query language (verified against this index)

| Pattern | Meaning |
|---|---|
| `term1 term2` | implicit AND |
| `"exact phrase"` | phrase match |
| `"two words"p3` | proximity, within 3 words |
| `term1 OR term2` | OR binds tighter than AND |
| `-term` | exclude |
| `ext:epub` / `ext:pdf` | filter by format |
| `dir:"/path/folder"` | restrict to a folder (reliable) |
| `title:word`, `author:name` | field search |
| `mime:application/pdf` | filter by MIME type |

Notes learned the hard way:
- `filename:` is unreliable for hyphenated names and does not match sub-documents.
  To restrict to one book, use `hits` (it filters by exact path internally), not a
  `filename:` query.
- Stemming is on by default, so `stoic` also matches `stoics`, `stoicism`. Quote a
  phrase to defeat it.
- EPUB "page" numbers are always `0` — EPUBs have no pages. Locate by chapter
  (`ipath`). PDF page numbers are real and map to `--page`.

## Working patterns

**Supplementing web research.** After a web pass on a topic with a durable core,
run a library pass for the foundation: web gives the current state, books give the
principle underneath. Present them separately — do not blend a 2015 book's claim
into a paragraph about this week's news.

**Finding a source for a claim.** When a draft asserts something that needs
backing, search the library for the concept, descend to level 3, and quote the
author. A real cited book beats a linked listicle in anything being published.

**Surveying a subject cold.** `search` broad, note which books recur across several
different queries — recurrence across phrasings is the strongest signal that a book
is genuinely about the topic rather than mentioning it.

**Reporting honestly.** If the library has nothing good on a topic, say so and
recommend the web instead. Even a large library has holes, and the failure mode
to avoid is stretching a weak book into a citation it does not support.
