# Quickstart – computer-use agent

```bash
docker build -t opsdesk-workforce-sample:3.2.0 docker
docker run --rm -p 8080:8080 -e OPSDESK_TASK=ow-e47b95f24436 -e OPSDESK_HOST_KEY=change-me \
  -v "$PWD/data/private/references:/srv/data/private/references:ro" opsdesk-workforce-sample:3.2.0
```

1. Open `http://localhost:8080` in the agent's browser (1280×800 or larger). The app needs no login and loads
   no external assets.
2. Give the agent the request text: `formats/harbor/<request>/instruction.md` (first paragraph) or
   `data/tasks/<request>/task.json` → `instruction`.
3. When the agent is done, score the workspace (host only):

```bash
curl -s -X POST -H "x-opsdesk-host-key: change-me" http://localhost:8080/host/finish
```

The answer contains `score.total_score` (0–1), every layer with details, and the state hash. Reset with
`POST /host/reset {"task_id": "..."}` (same header) for the next run.
