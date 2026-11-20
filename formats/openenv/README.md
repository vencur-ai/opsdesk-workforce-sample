# OpenEnv

The workspace as an OpenEnv-style environment: `POST /reset`, `POST /step`, `GET /state` (plus `GET /`, and
`GET /tasks` for the harness: it lists every request of the set and the public demo request, and needs the host key).

```
OPSDESK_TASK=<task id> OPSDESK_HOST_KEY=<secret for your harness> docker compose up -d
```

The agent reaches only `env` on `http://127.0.0.1:8000` (the app image, no References). The scoring service (the sealed
scoring image) is on an internal network; at `finish` the environment sends it the workspace record and passes on the
result. Neither the agent nor the environment ever sees a Reference.

- reset (harness only): `{"task_id": "<task id>"}` with the header `x-opsdesk-host-key: <secret>` → the request
  (`prompt`), the observation and the tools. Without the key the server refuses, so an agent cannot start a request again.
  Each reset starts a new workspace from the request's untouched files: the same state, mail and tool answers as a
  freshly started container, also after a finished run or another request (tested). One `env` container may therefore
  serve one attempt after another; one attempt at a time per container.
- step: `{"action": {"tool": "<tool name>", "args": {...}}}` → the tool's result
- finish: `{"action": {"tool": "finish"}}` → `reward` (0–1), `done: true`, `observation.passed` (= accepted),
  `accepted`, `strict` and per verifier layer passed and in full. No reference value is ever shown.
