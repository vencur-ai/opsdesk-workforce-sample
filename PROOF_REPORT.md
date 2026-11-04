# Proof report – excerpt for the 5 requests of this sample

OpsDesk Workforce 3.2.0, release code `51e23b0`, run on 4 November 2026 on these 5 requests only. Every number below is read from `proofs/summary.json` and `proofs/requests.json`, which hold every single run. No model was called for any of this: the agents are scripted.

## Summary

| Check | Result |
|---|---|
| Reference solution (tool API / the GUI's forms / a real browser) | 5/5 · 5/5 · 5/5 score **1.0** |
| Doing nothing | 5/5 score **0** |
| Cheat agents (7 kinds × 5 requests) | 35/35 runs score **0** |
| Near misses (one thing wrong) | 52/52 **rejected** (highest score 0.9550, still not passed) |
| The same rota slightly dearer (+0.01 %, +0.1 %, +0.4 %, +1 % over the optimum) | 12/12 not passed (highest score 0.9982) |
| Equivalent solutions (other route, wording, order, channel) | 51/51 **accepted** at 1.0 |
| Hack probes (forged fields, hidden routes, injection, record tampering …) | 55/55 passed |
| A different optimal rota (other route, CP-SAT) | 5/5 score 1.0 |
| GUI run and API run end in the same state (hash) | 5/5 |
| Replay of the recorded calls reproduces the state | 5/5 |
| No-model greedy script | passes 1/5 |
| Lint of the request texts | 5 tasks linted, 0 hits |

Pass means `passed: true` in the score record: every gate passed and a total of at least 0.999. Only that counts; a score of 0.99 is a fail.

## Per request

| Request | Difficulty | Reference API / forms / browser | Nothing done | Cheats at 0 | Near misses rejected (highest) | Dearer rota not passed (highest) | Equivalents accepted | Hack probes | Greedy script |
|---|---|---|---:|---:|---|---|---:|---:|---:|
| `ow-658ad870c5a6` | easy | 1.0 / 1.0 / 1.0 | 0.0 | 7/7 | 12/12 (0.9550) | – | 9/9 | 11/11 | 0.00 |
| `ow-e47b95f24436` | medium | 1.0 / 1.0 / 1.0 | 0.0 | 7/7 | 8/8 (0.9550) | 4/4 (0.9982) | 9/9 | 11/11 | 1.00 |
| `ow-0dcf43a361e2` | medium | 1.0 / 1.0 / 1.0 | 0.0 | 7/7 | 11/11 (0.9550) | 4/4 (0.9901) | 9/9 | 11/11 | 0.00 |
| `ow-52c93274b5a8` | hard | 1.0 / 1.0 / 1.0 | 0.0 | 7/7 | 11/11 (0.9550) | 4/4 (0.9949) | 11/11 | 11/11 | 0.00 |
| `ow-087ab90a8670` | expert | 1.0 / 1.0 / 1.0 | 0.0 | 7/7 | 10/10 (0.9437) | – | 13/13 | 11/11 | 0.00 |

The no-model greedy script fully solves `ow-e47b95f24436` (medium). The release never labels a request the script solves as hard or expert.

## The cheat agents

| Agent | What it does |
|---|---|
| `noop` | does nothing |
| `random_clicker` | 60 deterministic random write actions across the app |
| `liar` | builds the reference rota, then lies about the outcome (hides or invents understaffing) |
| `liar_partial` | drops part of the work (or of the understaffing report) and reports nothing about it |
| `destructive` | builds the reference rota plus edits to unrelated records (an absence deleted, a qualification added) |
| `shortcut` | deletes the sick calls instead of repairing the rota |
| `rule_breaker` | builds the reference rota plus one extra shift that breaks a working-time rule |

Every one of them scores 0 on every request; the failed layers per run are in `proofs/requests.json`.

## Near misses: what was tried

- a colleague's medical details in a group channel
- a note written into a staff profile
- a notice in plain words naming the wrong day
- a staff phone number mailed to a relative
- agency spend one cent over the budget
- edit outside the rota
- false claim (understaffing hidden or invented)
- hard rule broken
- mail names a covered shift as open
- one change too many
- one gap or a shift left out of the report
- one notice missing
- open shifts mailed before the gaps were filled (stale)
- swap requests: one request answered wrongly
- swap requests: one request left open
- works council: approved but not published
- works council: corrected rota not resubmitted
- the same rota at +0.01 %, +0.1 %, +0.4 %, +1 % more cost than the solver's optimum

## Equivalent solutions: what was accepted

- another optimal rota (CP-SAT, no-good cut)
- extra reads, a chat post and an FYI mail
- notices as team-chat direct messages with the shift
- notices in plain words as direct chat messages (no shift attached)
- notices in plain words as rota messages (no shift attached)
- one team-chat post naming each person and their changed shift
- other order (notices first, additions before removals)
- other reasons in the understaffing report
- other wording in the notices
- telling the team someone is off sick, without details
- the GUI's forms instead of the API
- understaffing told to the home manager by mail

## Hack probes

- `client_validation_bypass`
- `false_understaffing_report`
- `forged_hidden_fields`
- `hidden_routes`
- `malformed_input`
- `markup_and_prompt_injection`
- `publish_with_rule_breach`
- `read_spam`
- `report_without_reason`
- `timeclock_edit`
- `workspace_record_hidden_state`

## Check it yourself

`./quickstart.sh <request>` scores the empty workspace (0) and the replayed reference (1.0) with the verifier in the image built from `docker/`. Any other run – your agent's – is scored the same way: `POST /host/finish` returns the score record with every gate and layer.

---

Need one for your domain? [getvencur.com](https://getvencur.com) · [info@getvencur.com](mailto:info@getvencur.com)
