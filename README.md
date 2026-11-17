# OpsDesk Workforce 3.9 – sample

A verified workforce-operations environment: the HR and staffing back office of a shift-based employer under German labour law.

The first world is the staff office of a residential care provider. The agent works as the duty manager: it plans and
repairs the rota, answers swap and leave requests, handles sick calls and agency staff, and tells everyone whose shift
changed. Next to the rota the workspace has a mail client, a team chat and a calendar on one clock; colleagues answer
by fixed rules. Computer-use agents work in the browser; tool-use agents call the same functions over HTTP or MCP.
Both change one shared workspace. A deterministic verifier scores the end state – no language model judges.

The 5 requests in this sample have not been run on a model.

## Controls

| Control (on every one of the 5 requests) | Result |
|---|---|
| Reference solution – API, GUI forms, real browser | 5/5 · 5/5 · 5/5 score 1.0 |
| Reference solution in Docker – Harbor, plain HTTP | 5/5 · 5/5 score 1.0 |
| Doing nothing (host, Harbor, HTTP) | 5/5 score 0 |
| Liar: the same work, a false report (host, Harbor, HTTP) | 5/5 score 0 |
| Near misses: one rule broken · one coverable shift open · one change too many | 5/5 · 5/5 · 2/2 do not pass (an extra change is scored on the full-week repairs only – see CHECKS) |
| All near misses | 56/56 do not pass |
| Equivalent other solutions | 67/67 accepted (false accepts and false rejects: 0) |
| Hack probes | 55/55 passed |
| Greedy script, no model | 0/5 pass |

Every number per request: [`CONTROLS.md`](CONTROLS.md). What the verifier checks: [`CHECKS.md`](CHECKS.md).

## The 5 requests

All 5 use German labour law (working-time act, works council). They were generated for this sample from fresh seeds
and are in no other set.

| | Request id | Workflow | Law | Period | Staff | What the agent has to do |
|---|---|---|---|---|---:|---|
| R1 | `ow-89d72381a9ec` | Full week | German law | 28 days from 2026-10-23 | 81 | A week of incoming work in one go: sick calls (one arrives during the work), swap requests (one taken back later in the chat), an agency cancellation, a budget that is only given on request, a right-to-work reminder from HR, leave approved in the team chat. Keep the rota legal, covered and cheap, answer every request, tell everyone affected. |
| R2 | `ow-8e5b5092599c` | Full week | German law | 21 days from 2026-04-13 | 79 | A week of incoming work in one go: sick calls (one arrives during the work), swap requests (one taken back later in the chat), an agency cancellation, a budget that is only given on request, a right-to-work reminder from HR, leave approved in the team chat. Keep the rota legal, covered and cheap, answer every request, tell everyone affected. |
| R3 | `ow-1e3d8f52898d` | Build a rota | German law | 21 days from 2026-04-03 | 72 | Build the rota for the period from an empty plan: staff file, contracts, leave (one approval only in the team chat), a course day from the course list (with colleagues' spellings and a later correction), a right-to-work date, the works council's rules. |
| R4 | `ow-1e17253c0d81` | Document conflicts | German law | 21 days from 2026-10-13 | 72 | Bring the rota in line with documents that disagree: the course list and its correction, the staff file against an out-of-date HR reminder, leave approved only in the team chat. |
| R5 | `ow-7687d3080a92` | Document conflicts | German law | 21 days from 2026-01-21 | 75 | Bring the rota in line with documents that disagree: the course list and its correction, the staff file against an out-of-date HR reminder, leave approved only in the team chat. |

## Quick start (a few minutes, needs Docker)

1. Download the two images from this repository's release page and load them (app: 60 MB, sealed scoring image: 60 MB):

   ```bash
   docker load -i opsdesk-workforce_3.9.3-reviewer-sample.tar.gz
   docker load -i opsdesk-workforce-scoring_3.9.3-reviewer-sample.tar.gz
   ```

2. Start one workspace (one container per request; if port 8080 is taken on your machine, use another host port):

   ```bash
   docker volume create opsdesk-run
   docker run -d --name opsdesk -p 8080:8080 -e OPSDESK_TASK=ow-89d72381a9ec \
     -e OPSDESK_WORKSPACE_OUT=/workspace-out -v opsdesk-run:/workspace-out opsdesk-workforce:3.9.3-reviewer-sample
   until curl -sf http://127.0.0.1:8080/api/tools > /dev/null; do sleep 1; done
   ```

   Your agent works on `http://127.0.0.1:8080`: the app in a browser at `/`, or the tools – `GET /api/tools` lists
   them, `POST /api/step` with `{"tool": "requests.list", "args": {}}` calls one. MCP: `formats/mcp/README.md`. The
   request text is `instruction` in `data/tasks/ow-89d72381a9ec/task.json` (also `formats/harbor/ow-89d72381a9ec/instruction.md`).

3. Score it. Scoring ends the run (the container is stopped; a new run needs a new container and volume):

   ```bash
   docker stop opsdesk
   docker run --rm -v opsdesk-run:/in:ro opsdesk-workforce-scoring:3.9.3-reviewer-sample sh -c "python -m opsdesk.workforce.score_workspace \
     --tasks /srv/data/tasks --workspace /in/workspace.json --task ow-89d72381a9ec --out /tmp/s > /dev/null \
     && cat /tmp/s/reward.json /tmp/s/result.json"
   docker rm opsdesk && docker volume rm opsdesk-run
   ```

   `reward.json` (first line) is the score; `result.json` gives every layer and the reasons. An empty workspace scores
   `{"reward": 0.0, "passed": false, ...}`.

**Harbor:** `harbor run -p formats/harbor -a <your agent> --artifact /workspace-out/workspace.json`. The agent runs in its own
container without app code, task data or keys; the verifier runs in a separate container from the sealed scoring image.

**Acceptance check of the scoring image** (reference ≥ 0.999 and empty workspace 0 on all 5, without showing a solution):
`docker run --rm opsdesk-workforce-scoring:3.9.3-reviewer-sample python -m opsdesk.workforce.acceptance --tasks /srv/data/tasks`

## What is in this package

| Path | What |
|---|---|
| release page | the app image (no scoring code, no reference, no generator seed; it does hold the app's own logic, including the events it plays out during the work and the colleagues' rules) and the scoring image (the verifier and the reference solutions) |
| `data/tasks/` | the 5 requests as the app loads them |
| `formats/harbor`, `formats/http`, `formats/mcp` | Harbor tasks; HTTP and MCP notes |
| `manifest.json`, `SHA256SUMS` | contents and checksums |

**About the scoring image.** It holds the verifier and the reference solutions of these 5 requests, so anyone with
Docker can read them; the licence forbids it. For a blind evaluation on unseen requests the scoring stays with
Vencur: your agent runs on your side, you send the workspace records, Vencur returns the scores.

## Licence

Evaluation only – see [`LICENSE.md`](LICENSE.md). No training, no redistribution. Contact: info@getvencur.com
