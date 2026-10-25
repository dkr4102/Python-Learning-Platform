# Pip Learn implementation audit

Date: 24 October 2026 (Asia/Kolkata)

## Source of truth

Pip Learn currently contains two separate applications. They share branding and copied curriculum concepts, but they are not two builds of one runtime.

### Hosted website — authoritative for the current hosted product

- Checkout: `sites/pip-learn-studio`
- Git branch: `main`
- Audited hosted source commit: `57f688447fb63e33c709c9576b7246edd219b5a5`
- Framework: buildless HTML, CSS and browser JavaScript
- Entrypoint: `sites/pip-learn-studio/dist/index.html`
- State: browser `localStorage` under `pip-learn:variables-v2`
- Hosting manifest: `sites/pip-learn-studio/.openai/hosting.json`
- Sites project: `appgprj_6adcc680ad48819187bc0c795f60e9da`
- Live URL: `https://pip-learn-studio-2026.jollyibex8.chatgpt.site`
- Audience at audit time: custom access with the current user as owner

The Sites project and local nested checkout are linked: the local checkout HEAD matched the source commit opened from the hosted Sites repository. This is the implementation the user identified as the “new website.”

### Legacy Python application — separate local implementation

- Checkout: repository root `/Users/macbookair/PIP`
- Git branch: `master`
- Audited root commit: `58fc7bfd0a3427b1e98020a941a50fa615689c7c`
- Framework: NiceGUI, FastAPI/Uvicorn, SQLAlchemy and SQLite
- Entrypoint: `app/main.py`
- Default local URL: `http://127.0.0.1:8080`
- Persistence: `data/pip_learn.db`
- Routes: `/`, `/setup`, `/dashboard`, `/curriculum`, `/module/{id}`, `/module/{id}/lesson/{lesson_id}`, `/practice`, `/module/{id}/quiz`, `/projects`, `/achievements`, `/report`, `/settings`

This server is not the source deployed by the Sites manifest. Changes under `app/` do not change the hosted website.

## Hosted route inventory

The hosted website is a single static document. Its public navigation uses same-origin fragment links:

- `#home`
- `#curriculum`
- `#lesson`
- `#practice`
- `#quiz`

Stage selection is client-side and can also be requested with `?stage=read|watch|experiment|practice|check#lesson`.

No service worker, web app manifest, external application redirect, or hardcoded link to the local NiceGUI server was found. External links are limited to fonts, the YouTube thumbnail/player, and the explicitly labelled “Open on YouTube” fallback.

## Confirmed root causes

1. **Product duplication:** the root repository and nested Sites checkout are independent Git repositories and runtimes. The same visual/product name made them appear to be versions of one application.
2. **Hosted curriculum limitation:** the hosted Site contains an eight-module overview but only one implemented lesson workspace (Module 1, Variables). It does not currently consume the Python curriculum registry or SQLite records.
3. **Navigation ambiguity:** “Continue to next lesson” previously linked back to the same `#lesson` fragment, so it did not open a different lesson.
4. **Reading density:** the first reading page was intentionally short, but the complete Variables instruction was divided into only four mechanically grouped DOM slices. Important topics such as identifier rules and an applied example were not explicit sections.
5. **Video lifecycle:** the prior Play handler replaced markup with a raw iframe. It had no YouTube Player API lifecycle, no documented player-error handling, no `origin` identification, and did not request autoplay from the direct click.
6. **Execution boundary:** Experiment is a lesson-specific browser evaluator. It is not the subprocess runner from the NiceGUI application and cannot honestly be described as unrestricted or isolated Python execution.
7. **Persistence split:** hosted progress is browser-local; NiceGUI progress is SQLite. They are not synchronized.

## Unconfirmed hypotheses

- Browser caching may explain seeing an earlier hosted version immediately after publication, but no service worker or cache-owning application code exists in the hosted source.
- YouTube playback can still be affected by user browser policy, network filtering, video availability, or creator embedding restrictions. An HTTP 200 embed response alone does not prove media playback.

## Architecture decision

For this recovery, `sites/pip-learn-studio` is the authoritative source for the hosted website. The NiceGUI application is preserved as a separate legacy/reference implementation; it is not silently redirected, deleted, or presented as the deployed Site.

The current recovery fully hardens the implemented Variables lesson and shared stage shell. Migrating all 40 Python curriculum lessons and SQLite-backed business logic into the hosted runtime remains a distinct application-migration project, not a CSS repair.
