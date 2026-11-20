# Harbor

One Harbor task per request: `formats/harbor/<task id>/` with `task.toml`, `instruction.md`, `environment/` (the
agent's container `main` and the app container `app`, see `environment/docker-compose.yaml`), `tests/` (the verifier,
built `FROM` the sealed scoring image `opsdesk-workforce-scoring:3.12.5-sample-312en`) and `solution/`.

- `main` runs as an unprivileged user and holds no app code, no task data and no reference. It reaches the app at
  `http://app:8080` (browser GUI, `GET /api/tools`, `POST /api/step`) and keeps the default network for your model
  API; restrict its egress in your harness if your agent must not browse.
- `app` (`opsdesk-workforce:3.12.5-sample-312en`) sits on an internal network only and writes the workspace record into a volume that `main`
  mounts read-only.
- The verifier (`tests/test.sh`) replays the record in a separate container and writes `/logs/verifier/reward.json`
  and `result.json` (reward 0–1, passed (= accepted), accepted, strict, per layer passed and in full).
- `solution/solve.sh`: only the public demo request (`ow-cbddad055d16`) has a reference solution (its calls are in
  `demo/reference_calls.json`); for the requests of the set the solution stays sealed, and `solve.sh` says so and
  exits 1. An oracle trial therefore passes on the demo task only.

We ran these task folders with Docker Compose (build `main` and `app`, run the agent's calls from `main`, stop, build
`tests/`, run `test.sh`), not with the Harbor command-line tool itself.
