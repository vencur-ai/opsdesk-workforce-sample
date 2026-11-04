# Quickstart – OpsDesk Workforce sample

You need Docker (running), curl and Python 3. Nothing else is installed on your machine; the app runs offline in one
container per workspace.

## 1. One command

```bash
./quickstart.sh                    # default request ow-52c93274b5a8, port 8080
./quickstart.sh <request> [port]   # any of the five
```

It prints the score of the empty workspace (0, not passed) and of the replayed reference solution (1.0, passed).

The five requests:

- `ow-658ad870c5a6` – Swap requests (easy, UK)
- `ow-e47b95f24436` – Sick-call repair (medium, DE)
- `ow-0dcf43a361e2` – Works-council rejection (medium, DE)
- `ow-52c93274b5a8` – Agency budget (hard, UK)
- `ow-087ab90a8670` – Period that cannot be fully covered (expert, DE)

## 2. By hand: start a workspace

```bash
docker build -t opsdesk-workforce-sample:3.2.0 docker
docker run -d --name opsdesk -p 8080:8080 -e OPSDESK_TASK=ow-52c93274b5a8 -e OPSDESK_HOST_KEY=change-me \
  -v "$PWD/data/private/references:/srv/data/private/references:ro" opsdesk-workforce-sample:3.2.0
```

Open http://localhost:8080 – that is the screen a computer-use agent sees (1280×800 or larger). The request text is
in `data/tasks/<request>/task.json` → `instruction` (and in `formats/harbor/<request>/instruction.md`).

## 3. Connect your agent

- **Computer use:** give the agent the request text and a browser on http://localhost:8080.
- **Tools over HTTP:** `GET /api/tools` lists the tool schemas; `POST /api/step` with
  `{"tool": "roster.view", "args": {"summary_only": true}}` calls one. Mail, chat and calendar have their own tools.
- **MCP (stdio):** `python -m opsdesk.workforce.mcp --server http://localhost:8080`, run in `docker/runtime` after
  `pip install --require-hashes -r requirements.lock`.
- **Harbor / HUD / OpenEnv:** `formats/` (see `QUICKSTART_TOOLS.md`, `formats/hud/README.md`).

There is no report form: what the agent tells the home manager is what it does in the app (an understaffing report,
a decision on a request, a notice to a colleague).

## 4. Score

```bash
curl -s -X POST -H "x-opsdesk-host-key: change-me" -H "Content-Type: application/json" -d '{}' localhost:8080/host/finish
```

The answer holds `score.total_score` (0–1), `score.passed` (true only with every gate passed and at least 0.999),
every gate and layer with its details, and the state hash. Next run:

```bash
curl -s -X POST -H "x-opsdesk-host-key: change-me" -H "Content-Type: application/json" \
  -d '{"task_id": "ow-52c93274b5a8"}' localhost:8080/host/reset
docker rm -f opsdesk                # when you are done
```

The host key protects `/host/*`; the agent never needs it.
