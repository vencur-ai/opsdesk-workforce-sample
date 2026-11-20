# Plain HTTP (evaluation package)

The app image has no verifier and no reference; the sealed scoring image scores the workspace record afterwards.

1. One workspace per container (the record is rewritten after every call):

   ```
   docker volume create opsdesk-run
   docker run -d --name opsdesk -p 127.0.0.1:8080:8080 -e OPSDESK_TASK=<task id> \
     -e OPSDESK_WORKSPACE_OUT=/workspace-out -v opsdesk-run:/workspace-out opsdesk-workforce:3.12.5-sample-312en
   ```

2. Your agent works on `http://127.0.0.1:8080`:

| Who | Route | What |
|---|---|---|
| Computer-use agent | `GET /` (browser) | the OpsDesk Workforce app, 1280×800 or larger |
| Tool-use agent | `GET /api/tools` | tool schemas (same domain functions as the GUI) |
| Tool-use agent | `POST /api/step` | `{"tool": "roster.assign", "args": {...}}` |
| Tool-use agent | `GET /api/state` | the visible state of the home |

3. Score the record (deterministic: reward 0–1, passed (= accepted), accepted, strict, per layer passed and in full):

   ```
   docker stop opsdesk
   docker run --rm -v opsdesk-run:/in:ro opsdesk-workforce-scoring:3.12.5-sample-312en sh -c "python -m opsdesk.workforce.score_workspace \
     --tasks /srv/data/tasks --workspace /in/workspace.json --task <task id> --out /tmp/score > /dev/null; \
     rc=\$?; cat /tmp/score/reward.json /tmp/score/result.json; exit \$rc"
   ```

Without `OPSDESK_HOST_KEY` the host routes (`/host/*`) are off. If you set one, use a long random key: with it,
`/host/export` shows the hidden state (staged events, hidden budget). The app image cannot score.
