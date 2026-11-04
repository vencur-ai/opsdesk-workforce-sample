# Plain HTTP

Run one workspace: `docker run -p 8080:8080 -e OPSDESK_TASK=<task id> -e OPSDESK_HOST_KEY=<secret> opsdesk-workforce-sample:3.2.0`.

| Who | Route | What |
|---|---|---|
| Computer-use agent | `GET /` (browser) | the OpsDesk Workforce app, 1280×800 or larger |
| Tool-use agent | `GET /api/tools` | tool schemas (same domain functions as the GUI) |
| Tool-use agent | `POST /api/step` | `{"tool": "roster.assign", "args": {...}}` |
| Tool-use agent | `GET /api/state` | the visible state of the home |
| Host | `POST /host/reset` | `{"task_id": ...}` – fresh workspace (`x-opsdesk-host-key`) |
| Host | `POST /host/finish` | claims from in-app actions → deterministic score (reference must be mounted at `/srv/data/private/references`) |
| Host | `GET /host/state-hash`, `GET /host/export` | state hash, full export for host scoring |
