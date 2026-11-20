# Proof Report – OpsDesk Workforce – private set sample-312en

Release 3.12.4 · 5 requests and one public demo request · deterministic verifier, no language-model judge.

## Identity

| | |
|---|---|
| Version | 3.12.4 |
| Source tag | v3.12.4 |
| Source commit | 14170df1740c4dde57467be40eb612167b67a248 |
| SHA-256 of the source at the tag (git archive, tar) | 7e0874d34d1f2984335a91967e489981c879f4bde15d90f88da4455f7ceaabe3 |
| Image opsdesk-workforce-scoring:3.12.4-sample-312en (linux/amd64) | sha256:c28f6771bd783247ea489e946f22bff975f995c2d4b1e08fe15c905768850818 |
| Image opsdesk-workforce-scoring:3.12.4-sample-312en (linux/arm64) | sha256:9c46b66cfe4be76e3b5e0a90b7827f99ca3f06ba3ba549f5cbb68981f9f4131a |
| Image opsdesk-workforce:3.12.4-sample-312en (linux/amd64) | sha256:2cab8115259d0f7c8e724a66109ee10c7de2cce45e7304d8b2fd56425bfba31e |
| Image opsdesk-workforce:3.12.4-sample-312en (linux/arm64) | sha256:e15b41d74af7793798e8e4a1390241c29168b73ebadcec7236df98bc864add16 |

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
