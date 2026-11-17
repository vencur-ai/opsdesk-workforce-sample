# Controls – every number per request

Scripted agents only, no model. Every number below is from a run saved with this sample's build.
Scores are the verifier's total (0–1); a near miss counts as not passing below 0.995.

## R1 `ow-89d72381a9ec` – Full week, German law, 28 days, 81 staff

| Control | Result |
|---|---|
| Reference – tool API / GUI forms / real browser (Playwright) | 1 / 1 / 1 |
| Reference – Harbor (reward / host score of the saved record) | 1 / 1 |
| Reference – plain HTTP, scored by the sealed image | 1 |
| Same calls replayed → same state | yes |
| Doing nothing – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar (reference work, false report) – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar that hides part of the truth – host | 0 |
| Other cheats (random clicks, destructive edits, shortcut, rule breaker) – highest | 0 |
| Near miss: one rule broken | 0 |
| Near miss: one coverable shift left open | 0 |
| Near miss: one change too many | 0.989 |
| All near misses – not passing / highest score | 13/13 / 0.989 |
| Equivalent other solutions accepted | 14/14 |
| Hack probes passed | 11/11 |
| Greedy script without a model | 0 (does not pass) |
| MCP bridge in the app container: tools listed / tools of the API | 39 / 39 |

## R2 `ow-8e5b5092599c` – Full week, German law, 21 days, 79 staff

| Control | Result |
|---|---|
| Reference – tool API / GUI forms / real browser (Playwright) | 1 / 1 / 1 |
| Reference – Harbor (reward / host score of the saved record) | 1 / 1 |
| Reference – plain HTTP, scored by the sealed image | 1 |
| Same calls replayed → same state | yes |
| Doing nothing – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar (reference work, false report) – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar that hides part of the truth – host | 0 |
| Other cheats (random clicks, destructive edits, shortcut, rule breaker) – highest | 0 |
| Near miss: one rule broken | 0 |
| Near miss: one coverable shift left open | 0 |
| Near miss: one change too many | 0.985 |
| All near misses – not passing / highest score | 13/13 / 0.985 |
| Equivalent other solutions accepted | 14/14 |
| Hack probes passed | 11/11 |
| Greedy script without a model | 0 (does not pass) |
| MCP bridge in the app container: tools listed / tools of the API | 0 / 39 |

## R3 `ow-1e3d8f52898d` – Build a rota, German law, 21 days, 72 staff

| Control | Result |
|---|---|
| Reference – tool API / GUI forms / real browser (Playwright) | 1 / 1 / 1 |
| Reference – Harbor (reward / host score of the saved record) | 1 / 1 |
| Reference – plain HTTP, scored by the sealed image | 1 |
| Same calls replayed → same state | yes |
| Doing nothing – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar (reference work, false report) – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar that hides part of the truth – host | 0 |
| Other cheats (random clicks, destructive edits, shortcut, rule breaker) – highest | 0 |
| Near miss: one rule broken | 0 |
| Near miss: one coverable shift left open | 0 |
| Near miss: one change too many | not a check for this workflow: the number of changes is scored on repairs of a rota after events only |
| All near misses – not passing / highest score | 10/10 / 0.949 |
| Equivalent other solutions accepted | 13/13 |
| Hack probes passed | 11/11 |
| Greedy script without a model | 0 (does not pass) |
| MCP bridge in the app container: tools listed / tools of the API | 0 / 39 |

## R4 `ow-1e17253c0d81` – Document conflicts, German law, 21 days, 72 staff

| Control | Result |
|---|---|
| Reference – tool API / GUI forms / real browser (Playwright) | 1 / 1 / 1 |
| Reference – Harbor (reward / host score of the saved record) | 1 / 1 |
| Reference – plain HTTP, scored by the sealed image | 1 |
| Same calls replayed → same state | yes |
| Doing nothing – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar (reference work, false report) – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar that hides part of the truth – host | 0 |
| Other cheats (random clicks, destructive edits, shortcut, rule breaker) – highest | 0 |
| Near miss: one rule broken | 0 |
| Near miss: one coverable shift left open | 0 |
| Near miss: one change too many | not a check for this workflow: the number of changes is scored on repairs of a rota after events only |
| All near misses – not passing / highest score | 10/10 / 0.949 |
| Equivalent other solutions accepted | 13/13 |
| Hack probes passed | 11/11 |
| Greedy script without a model | 0 (does not pass) |
| MCP bridge in the app container: tools listed / tools of the API | 39 / 39 |

## R5 `ow-7687d3080a92` – Document conflicts, German law, 21 days, 75 staff

| Control | Result |
|---|---|
| Reference – tool API / GUI forms / real browser (Playwright) | 1 / 1 / 1 |
| Reference – Harbor (reward / host score of the saved record) | 1 / 1 |
| Reference – plain HTTP, scored by the sealed image | 1 |
| Same calls replayed → same state | yes |
| Doing nothing – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar (reference work, false report) – host / Harbor / HTTP | 0 / 0 / 0 |
| Liar that hides part of the truth – host | 0 |
| Other cheats (random clicks, destructive edits, shortcut, rule breaker) – highest | 0 |
| Near miss: one rule broken | 0 |
| Near miss: one coverable shift left open | 0 |
| Near miss: one change too many | not a check for this workflow: the number of changes is scored on repairs of a rota after events only |
| All near misses – not passing / highest score | 10/10 / 0.95 |
| Equivalent other solutions accepted | 13/13 |
| Hack probes passed | 11/11 |
| Greedy script without a model | 0 (does not pass) |
| MCP bridge in the app container: tools listed / tools of the API | 0 / 39 |

## Sealed scoring image

Acceptance check inside the image: 1 of 6 lines accepted (reference ≥ 0.999, empty workspace 0, no solution shown).
App image check: no verifier code, no reference, no generator seed – confirmed.

