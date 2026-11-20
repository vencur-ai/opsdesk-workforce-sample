# Proof Report – OpsDesk Workforce – private set sample-312en

Release 3.12.5 · 5 requests and one public demo request · deterministic verifier, no language-model judge.

## Identity

| | |
|---|---|
| Version | 3.12.5 |
| Source tag | v3.12.5 |
| Source commit | fff58b49626fe3e57110db09b541d7232113a485 |
| SHA-256 of the source at the tag (git archive, tar) | a3867f03bf9e4abbb19bba0febc512f77fc79496b34a01ac9f27812aa18ced76 |
| Image opsdesk-workforce-scoring:3.12.5-sample-312en (linux/amd64) | sha256:0a87a8298b6b786c4db5edaf832267b4778ac2f5efa449a015d5a1ca73131f67 |
| Image opsdesk-workforce-scoring:3.12.5-sample-312en (linux/arm64) | sha256:73c38f0f69d7901caa2b97066a333f4eb5471f45b645ebc932166b0fe5bebcac |
| Image opsdesk-workforce:3.12.5-sample-312en (linux/amd64) | sha256:e407d4b56597d92daa101a335c55f8eab8fc99204e9e6f5b1f088d10b23eae42 |
| Image opsdesk-workforce:3.12.5-sample-312en (linux/arm64) | sha256:f6f46c4a04f84283bc10c1869c4275f9ea79b5167619a7c5e7d81e4b3153d0b8 |

The SHA-256 of every file of the package is in `SHA256SUMS`; `docker image inspect` shows each image's ID.

## Controls you can re-run

Every number below is the output of the sealed acceptance check in the scoring image, on the delivered images
(linux/amd64, linux/arm64; the same numbers on each). The command reproduces it; it
shows scores and yes/no only, never a solution.

| Control | Result | Re-run |
|---|---|---|
| (a) Every request loads in a fresh workspace and answers | 5/5 | `docker run --rm <scoring image> python -m opsdesk.workforce.acceptance --check load` |
| (b) Replaying a run's calls gives the same state and the same score | 5/5 | `docker run --rm <scoring image> python -m opsdesk.workforce.acceptance --check replay` |
| (c) The References score at least 0.999 and pass | 5/5 | `docker run --rm <scoring image> python -m opsdesk.workforce.acceptance --check reference` |
| (d) An empty run scores 0 | 5/5 | `docker run --rm <scoring image> python -m opsdesk.workforce.acceptance --check cheats` |
| (d) The reference work plus a false understaffing report scores 0 | 5/5 | `docker run --rm <scoring image> python -m opsdesk.workforce.acceptance --check cheats` |
| (d) The reference work plus an edit outside the request scores 0 | 5/5 | `docker run --rm <scoring image> python -m opsdesk.workforce.acceptance --check cheats` |
| (d) The reference work plus a final status report with one wrong field scores 0 | 40/40 | `docker run --rm <scoring image> python -m opsdesk.workforce.acceptance --check cheats` |
| (d) The reference work plus the true status report again (with any note) keeps its result | 10/10 | `docker run --rm <scoring image> python -m opsdesk.workforce.acceptance --check cheats` |

## Formats run end to end on the delivered images

The public demo request (`demo/`), its reference calls sent through each format, the record scored by the scoring
image (linux/arm64).

| Format | How | Result |
|---|---|---|
| HTTP | plain HTTP → app container | reward 1.0, passed yes |
| MCP | MCP bridge (stdio) → app container | reward 1.0, passed yes |
| OpenEnv | OpenEnv server in the app image → scoring service (internal network) | reward 1.0, passed yes |
| Harbor | Harbor task files with Docker Compose (app, main, verifier image from tests/; not the Harbor tool) | reward 1.0, passed yes |

## Also checked before delivery (not re-runnable from this package)

The same requests also went through checks that need the solver, a browser or the solutions in plain text: the
reference work through the GUI forms and a real browser, near misses one change away from the solution, equivalent
solutions, other valid rotas from the solver, hack probes and a greedy script without a model. They carry no number
here because you cannot re-run them from the package.

## Model success rates

Not yet measured for the English edition.
