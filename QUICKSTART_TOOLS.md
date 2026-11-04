# Quickstart – tool-use agent (HTTP or MCP)

Start a workspace as in `QUICKSTART_COMPUTER_USE.md`, then:

```bash
curl -s http://localhost:8080/api/tools                         # tool schemas
curl -s -X POST http://localhost:8080/api/step -H 'Content-Type: application/json' \
  -d '{"tool": "roster.view", "args": {"include_honesty_summary": true, "summary_only": true}}'
```

MCP (stdio), same workspace: `python -m opsdesk.workforce.mcp --server http://localhost:8080`
(run in `docker/runtime` after `pip install --require-hashes -r requirements.lock`).

There is no report form: what the agent tells the home manager is what it does in the app – e.g.
`reports.understaffing` for shifts that cannot be covered, `requests.decide` for swap requests, `messaging.send`
with shift fields for notices. The office apps have their own tools: `mail.list`, `mail.read`, `mail.attachment`,
`mail.send`, `mail.contacts`, `chat.channels`, `chat.read`, `chat.post`, `calendar.list`, `calendar.create` – a reply to
a mail is `mail.send` with `in_reply_to`, a course day is a `calendar.create` entry with its attendees. Colleagues
answer chat posts and mails in the same step. Score with `POST /host/finish` (host key).

Harbor: each folder under `formats/harbor/` is a task (`instruction.md`, `task.toml`, `environment/`,
`solution/solve.sh` replays the gold calls). The app writes its workspace record after every call into a volume the
agent's container can only read; Harbor collects it (`artifacts`) and scores it in a separate verifier container built
from `tests/` (`[verifier] environment_mode = "separate"`), which replays the record and writes
`/logs/verifier/reward.json`. The agent's container holds no app code, task data, reference or key. The app and
verifier images start from the workspace image, so build it once before the first run:
`docker build -t opsdesk-workforce-sample:3.2.0 docker/`.
