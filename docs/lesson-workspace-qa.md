# Hosted lesson workspace QA

Date: 24 October 2026 (Asia/Kolkata)

## Scope

Authoritative hosted checkout: `sites/pip-learn-studio`. Reference lesson: Module 1, Variables.

## Defects reproduced

- Two unrelated Pip Learn implementations were reachable under local and hosted URLs.
- The hosted first reading section did not by itself teach the concept.
- Reading pages were produced by brittle DOM slicing rather than explicit teaching objectives.
- Video Play created an iframe without Player API error reporting.
- Completion’s “next lesson” action returned to the same lesson.
- Experiment publicly called itself a “static prototype.”

## Test matrix and actual outcomes

| Test | Outcome |
|---|---|
| Hosted repository identity and manifest | Passed; Sites project and nested checkout matched. |
| Same-origin hosted navigation audit | Passed; no links to `127.0.0.1` or the legacy application. |
| Direct `/` load from local static server | Passed, HTTP 200. |
| Read, Watch, Experiment, Practice and Check deep links | Passed, HTTP 200 for each query/fragment entry. |
| Variables reading sections | Passed after reconstruction; six sections are reachable and browser state is persisted. |
| Practice draft switching | Passed by source and browser inspection; each task keeps separate browser state. |
| Practice success/failure evaluator | Passed for provided positive and negative patterns. |
| Check answer persistence and retry | Passed by source inspection and manual browser interaction. |
| Refresh/resume | Passed for saved stage, reading page, editors, notes and answers via localStorage. |
| YouTube thumbnail | Passed; genuine thumbnail returned HTTP 200. |
| YouTube embed endpoint | Passed with HTTP 200 and same-origin Referer. |
| Actual media playback | Not fully automatable in the available Safari setup because JavaScript automation from Apple Events was disabled. Manual test instructions are below. |
| Desktop visual inspection | Passed at a large desktop Safari window; no clipped primary controls in the recovered workspace. |
| Narrow-window inspection | Passed; content stacks and document scrolling is used. Exact device emulation was unavailable. |

## Manual YouTube playback test

1. Open the deployed Site and enter the Variables lesson.
2. Select **02 Watch**.
3. Confirm the Corey Schafer thumbnail and title are visible.
4. Press the centred Play button once.
5. Confirm native YouTube controls replace the thumbnail.
6. If the player reports errors 5, 100, 101, 150 or 153, confirm the explanation and **Watch on YouTube** fallback remain visible.
7. Switch to Experiment and back to Watch; notes and watch status must remain saved.

## Remaining limitations

- The hosted Site implements one complete lesson workspace, not all 40 curriculum lessons.
- Its guided evaluator and pattern-based practice tests are intentionally limited browser-side evaluators, not the NiceGUI subprocess runner.
- Browser-local progress is not synchronized with the legacy SQLite database.
- Exact automated screenshots at every requested viewport were not available; desktop and narrow-window browser inspection was performed.
