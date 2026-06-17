# Debug & Research

The anti-"it's impossible" workflow. Triggered when every available rung or handler has failed. It diagnoses the *actual* cause from the error log and researches a concrete workaround instead of giving up. It ends in one of three states: content retrieved, a new handler proposed, or a single honestly-documented dead end — never a reflexive "can't be done."

**Inputs:** the URL, the extraction hint (if any), and the full error log from the failed ladder/handler.
**Prerequisites:** none.

Read `references/tool-cheatsheet.md` (failure-signal definitions) and `references/handler-registry.md` (so a proposal slots into the real extension point).

---

## Step 1 — Diagnose

**Goal:** Name the real failure mode, not a vague one.

1. Read the error log. Classify what actually happened using the cheatsheet's signal categories: HTTP block (403/429/503), JS-required shell, paywall/consent gate, CAPTCHA/bot challenge, or plain tool error/timeout.
2. State the diagnosis in one line. The fix depends on the category — a 429 is a rate-limit (slow down / change UA), a JS-shell is a render problem (already tried playwright → look for an API), a paywall is a content-gate (look for archive/print/AMP/API).

**Output:** a one-line diagnosis naming the category.

---

## Step 2 — Research workarounds

**Goal:** Find how others fetch *this kind* of resource. Use WebSearch and reasoning. Match tactics to the diagnosed category:

- **Hidden / unofficial API or data endpoint.** Many sites back their UI with a JSON API (XHR endpoints, `/api/`, `.json` suffixes, GraphQL, an `__NEXT_DATA__` / `window.__INITIAL_STATE__` blob in the HTML). Look for it. This is how the Reddit handler was born.
- **Official API + library.** Search "<site> API" and "<site> python library" (the PRAW-for-Reddit pattern). A maintained client usually beats scraping.
- **Alternate host / cached copy.** `old.` subdomains, `m.` mobile, AMP pages, print views, Google cache, the Wayback Machine (`web.archive.org`), text-only mirrors.
- **Header / UA / cookie tweak.** A descriptive User-Agent, an `Accept` header, a referer, or a consent cookie often clears a soft block.
- **Rate-limit handling.** For 429s: back off, slow the request rate, or rotate UA.
- **Proxy / residential egress.** Last resort for hard IP blocks — note it as a future capability if nothing else works (this is a known planned extension, not yet built).

Run the searches. Read what real people did. Do not conclude "impossible" until you've actually looked.

**Output:** one or more candidate tactics, ranked by effort.

---

## Step 3 — Attempt the top candidate

**Goal:** Actually try the most promising workaround.

1. Implement the top-ranked tactic (call the discovered endpoint, install the library, hit the archive, add the header, etc.).
2. Evaluate the result against the cheatsheet failure signals.
3. If it worked → go to Step 4. If not, log it and try the next candidate. Exhaust the reasonable candidates before Step 5.

**Output:** retrieved content, or an updated log of what else was tried.

---

## Step 4 — Deliver + propose a handler

**Goal:** Give the user the content AND make the win permanent.

1. Return the content (narrowed to the hint if given).
2. If the working tactic was domain-specific (an API, a library, a host trick that will recur), propose registering it: state the exact row to add to `references/handler-registry.md` and a sketch of the `workflows/handlers/<name>.md` file. Offer to write it now so this site never fails again.

**Output:** content + (when applicable) a concrete handler proposal. Workflow ends.

---

## Step 5 — Honest dead end (rare)

**Goal:** If — and only if — every researched tactic genuinely failed, report precisely.

1. Tell the user exactly what was tried (the full log) and the specific blocker that remains (e.g. "hard IP block, needs a residential proxy we haven't added yet").
2. Frame it as a missing capability with a named next step (e.g. "add proxy support to the ladder"), not as "this is impossible." The skill is extensible; the gap is the answer.

**Output:** a precise, actionable status — what's blocking and what would unblock it.

---

## Done

This workflow is complete when:
- [ ] The content was retrieved via a workaround, OR
- [ ] A working tactic was found and a concrete handler was proposed/registered, OR
- [ ] A specific, named blocker was reported with the concrete capability that would resolve it — never a bare "can't be done."
