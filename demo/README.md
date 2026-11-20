# Demo: check the scoring yourself

`ow-cbddad055d16` is a public demo request. It is not part of your set, and no model has seen it. Its reference
calls are in `reference_calls.json`. Run them through the app and score the workspace record with the sealed
scoring image. The demo should score 1.0, and a run that does nothing scores 0.

```bash
docker load -i ../images/opsdesk-workforce_3.12.4-sample-312en_amd64.tar        # or _arm64.tar on Apple silicon / ARM servers
docker load -i ../images/opsdesk-workforce-scoring_3.12.4-sample-312en_amd64.tar
sh run_demo.sh            # PORT=8080 by default
```

What `run_demo.sh` does:

1. **Start a fresh app container** for the demo request: `opsdesk-workforce:3.12.4-sample-312en`. It writes its workspace record after every call.
2. **Send the reference calls** to `POST /api/step`, as an agent's tool calls would arrive.
3. **Stop the app.** The record holds only the call log and the final state hash.
4. **Score the record** with `opsdesk-workforce-scoring:3.12.4-sample-312en`: `score_workspace` replays the calls, checks the hash and scores. The
   result is `"reward": 1.0`.
5. **Do it again without any call:** `"reward": 0.0`.
