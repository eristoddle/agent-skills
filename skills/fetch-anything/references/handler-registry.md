# Handler Registry

Domain → custom-handler lookup. The router reads this at intake. If the target URL's host matches a `match` pattern below, the router loads the named handler workflow instead of the generic `fetch-ladder.md`.

**This is the extension point.** To make `fetch-anything` handle a new site specially, add a row here and create the matching file under `workflows/handlers/`. Nothing else changes.

---

## Registry

| match (host contains) | handler file | why it needs special handling |
|---|---|---|
| `reddit.com`, `redd.it` | `workflows/handlers/reddit.md` | HTML is JS-rendered and rate-limited; tries `.json` endpoint first (often 403 now), then crawl4ai stealth browser on old.reddit.com. |

---

## How matching works

- Compare against the URL's **host** (and path where noted), case-insensitive.
- `match` is a substring/host test, not a full regex — keep patterns simple (`reddit.com` matches `www.reddit.com`, `old.reddit.com`, `np.reddit.com`).
- First matching row wins. Order more specific patterns above broader ones.
- No match → generic `workflows/fetch-ladder.md`.

## Adding a handler (checklist)

1. Add a row above: the host pattern, the handler path, and a one-line reason.
2. Create `workflows/handlers/<name>.md` following the structure of `reddit.md`: state inputs, the ordered attempts (cheapest/no-auth first), escalation, and done criteria.
3. The handler should still end by handing terminal failures to `workflows/debug-research.md`.
