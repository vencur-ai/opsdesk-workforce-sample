#!/bin/sh
# Demo: app -> workspace record -> score, with the public demo request and its reference calls.
set -e
cd "$(dirname "$0")"
APP=opsdesk-workforce:3.12.5-sample-312en; SCORING=opsdesk-workforce-scoring:3.12.5-sample-312en; TASK=ow-cbddad055d16; PORT=${PORT:-8080}
run() {  # $1: calls file (reference) or empty (no call)
  docker volume create opsdesk-demo >/dev/null
  docker run -d --name opsdesk-demo -p 127.0.0.1:$PORT:8080 -e OPSDESK_TASK=$TASK \
    -e OPSDESK_WORKSPACE_OUT=/workspace-out -v opsdesk-demo:/workspace-out $APP >/dev/null
  i=0; until curl -sf http://127.0.0.1:$PORT/api/tools >/dev/null; do i=$((i+1)); [ $i -gt 120 ] && exit 1; sleep 1; done
  if [ -n "$1" ]; then
    docker exec -i opsdesk-demo python -m opsdesk.workforce.oracle --url http://127.0.0.1:8080 --calls /dev/stdin < "$1"
  fi
  docker stop opsdesk-demo >/dev/null
  docker run --rm -v opsdesk-demo:/in:ro $SCORING python -m opsdesk.workforce.score_workspace \
    --tasks /srv/data/tasks --workspace /in/workspace.json --out /tmp/out --task $TASK
  docker rm opsdesk-demo >/dev/null; docker volume rm opsdesk-demo >/dev/null
}
echo "reference calls:"; run reference_calls.json
echo "no call:"; run ""
