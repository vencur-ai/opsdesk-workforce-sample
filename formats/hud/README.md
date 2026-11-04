# HUD environment (computer-use + MCP) – not deployed

- `env.py`: one template `workspace(task_id)`; starts the OpsDesk Workforce app, a headless Chromium on the app
  (capability `browser`, CDP) and the same functions as MCP tools (capability `tools`). Reward = deterministic
  verifier score at the end (claims from in-app actions, strict honesty).
- Build context: this folder plus `runtime/` (the `opsdesk` package of release 3.2.0) and `data/`
  (tasks, host data and – training licence or public sample – the references). `data/` is assembled at listing time
  with `python -m opsdesk.workforce.export --candidate <set> --out <dir> --licence training --delivery <name>`;
  references stay inside the container, the agent only sees the browser and the tools. The grade frame is the score
  as a number with `passed` and `scored` in `info`; an evaluation delivery (no references) returns the placeholder
  0.0 with `scored: false` (3.1.5).
- **Build instructions only.** Vencur ships no prebuilt HUD image; your build fetches the packages in `uv.lock`.
  The HUD SDK needs `asyncvnc` (GNU GPL v3) and `asyncssh` (EPL-2.0 or GPL-2.0-or-later; Vencur uses it under
  EPL-2.0); every licence is listed in `THIRD_PARTY_LICENSES.md` of the release.
- Local dry run with the HUD SDK, no account, nothing uploaded: `OPSDESK_CHROMIUM=<chromium> python hud_dryrun.py`
  (needs `data/private/references` for the gold replay).
