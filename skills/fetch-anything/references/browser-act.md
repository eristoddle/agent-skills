# Rung 5 — browser-act (embedded, UNTESTED)

The last rung of the fetch ladder. A full browser-automation CLI for AI agents:
anti-detection rendering, captcha bypass, persistent multi-account sessions,
proxy support, network/HAR capture, and human-in-the-loop assist. It is the most
capable tool in the ladder and the most heavyweight — only reach for it after
defuddle, webfetch, crawl4ai, and playwright-cli have all failed.

⚠️ **UNTESTED in this skill.** It was added because it *should* defeat pages the
proven rungs can't (hard bot walls, captcha gates, login-walled JS apps). If it
misbehaves, log the result and fall through to `workflows/debug-research.md`.
Don't let an unproven tool turn into a rabbit hole.

> Embedded from the upstream `browser-act` SKILL.md (BrowserAct, v2.0.2). The CLI
> is already installed on this machine (`browser-act` on PATH). Authoritative,
> always-current usage lives behind `get-skills core` (Step 0 below) — this file
> is the entry contract, not a full command reference.

---

## What it offers (relevant to fetching)

- **Lightweight extraction** — `stealth-extract <url>`: fast, anti-detection,
  JS-rendered content fetch **without opening a browser session**. Positioned by
  the vendor as an "advanced WebFetch/curl replacement." This is the cheap path
  and the first thing to try at this rung — no browser creation, no confirmation.
- **Session management** — multi-browser isolation, multi-account parallel runs.
- **Verification assistance** — `solve-captcha` / `captcha-aid` for interactive
  challenges (sends only the challenge image; no cookies or page content).
- **Complex interaction** — navigate, click, input, `get markdown`, `get html`,
  screenshots, form filling, file upload.
- **Human-agent collaboration** — headed mode + `remote-assist` hands the user a
  link to drive the browser through a manual step.
- **Proxy + network** — configured proxies, `network requests`, HAR export.

## Data & safety posture

- **Local-only.** All cookies, sessions, page content, credentials, and profile
  data are stored and processed locally — never uploaded. The only outbound data
  is the captcha challenge image, and only when `solve-captcha` is invoked.
- **Confirmation Gate.** browser-act requires **explicit user approval before**
  creating a browser, deleting one, or any sensitive operation (login, form
  submission, file upload). `stealth-extract` does NOT create a browser, so it
  needs no confirmation; escalating to a full session DOES — ask first.

---

## How to use it at this rung

### Step 0 — Mandatory bootstrap (do NOT skip, do NOT truncate)

Before running *any* other `browser-act` command:

```bash
browser-act get-skills core --skill-version 2.0.2
```

This returns environment status, available browsers, operational directives, the
browser-selection rules, and the full interaction workflow — none of which are in
`--help`. Skipping it or truncating its output means missing safety constraints
and selection rules. Read it, then proceed.

### Step 1 — Cheap path: stealth-extract (no session, no confirmation)

```bash
browser-act stealth-extract "<URL>"
# Useful flags (see get-skills core / --help for the full set):
#   --content-type     narrow what gets extracted
#   --render-wait      wait longer for JS to settle
#   --timeout          cap the attempt
#   --output           write to a file
#   --static-proxy / --dynamic-proxy / --custom-proxy   route through a proxy
```

If this returns real content, you're done — deliver it (ladder Step 6).

### Step 2 — Escalate inside browser-act (ONLY with user confirmation)

If `stealth-extract` is still blocked and the content justifies a full session:

1. **Confirm with the user** before creating a browser (Confirmation Gate).
2. Create/open a browser and navigate:
   ```bash
   browser-act browser create --type ... --name fetch
   browser-act --session fetch browser open <id> "<URL>"
   browser-act --session fetch wait stable
   browser-act --session fetch get markdown
   ```
3. On a captcha/challenge: `browser-act --session fetch solve-captcha`
   (or `captcha-aid`).
4. If a human must step in: `browser-act --session fetch remote-assist --objective "..."`
   and hand the user the link.
5. Close the session when done: `browser-act --session fetch session close`.

The exact session/browser selection rules come from `get-skills core` — defer to
it over this sketch if they differ.

---

## Failure → fall through

A browser-act result counts as **failed** under the same signals as the rest of
the ladder (empty body, persistent block/captcha, tool error, timeout). When it
fails — or errors in any unexpected way, since it's untested — append a line to
the error log and go to `workflows/debug-research.md` (ladder Step 7). Never
report a bare failure to the user from here.

```
- browser-act: <stealth-extract empty / still blocked / CLI missing / errored: ... / ok>
```

---

## Reference

- Homepage: https://www.browseract.com
- Install (already done here): `uv tool install browser-act-cli --python 3.12`
- Upstream skill: https://github.com/browser-act/skills/blob/main/browser-act/SKILL.md
