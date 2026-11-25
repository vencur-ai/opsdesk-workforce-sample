#!/bin/sh
# One-command quick start: download the two images for this machine from the release, check them against the SHA-256
# values below, load them into Docker and run the demo (reference calls score 1.0, no call scores 0).
# Needs Docker, curl and about 250 MB of free disk. Images you already have locally: RELEASE_DIR=<folder> sh quickstart.sh
set -e
cd "$(dirname "$0")"
VER=3.13.1-sample-313en
BASE=https://github.com/vencur-ai/opsdesk-workforce-sample/releases/download/v3.13.1-sample

case "$(uname -m)" in
  x86_64|amd64) ARCH=amd64 ;;
  arm64|aarch64) ARCH=arm64 ;;
  *) echo "Unsupported machine: $(uname -m). Images exist for amd64 and arm64." >&2; exit 1 ;;
esac
command -v docker >/dev/null 2>&1 || { echo "Docker is needed: https://docs.docker.com/get-docker/" >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "Docker is installed but not running. Start it and try again." >&2; exit 1; }

expected() {  # SHA-256 of each release image (the same values as SHA256SUMS_RELEASE on the release page)
  case "$1" in
    opsdesk-workforce_${VER}_amd64.tar)         echo 12aff5200a2f39760e6b342a30f4226f764f39a73f9cedc7147fa3dd2b3d8867 ;;
    opsdesk-workforce-scoring_${VER}_amd64.tar) echo 317ff442ec85b5fec56c1b7716918c2280a43ac0f6bd9aaa9634512c64c08fd4 ;;
    opsdesk-workforce_${VER}_arm64.tar)         echo 6a7dd2122de281471c71e7ed2d4c589aa4f5c4a0c00b627b305df916df412030 ;;
    opsdesk-workforce-scoring_${VER}_arm64.tar) echo 1813feb57ed9994cd1399ae27fc6b89b709d974fc540c48f78932025a3c2f364 ;;
  esac
}
sha() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1"; else shasum -a 256 "$1"; fi | cut -d' ' -f1; }

if [ -n "$RELEASE_DIR" ]; then DIR=$RELEASE_DIR; else DIR=${XDG_CACHE_HOME:-$HOME/.cache}/opsdesk-workforce-sample/$VER; fi
mkdir -p "$DIR"
for f in "opsdesk-workforce_${VER}_$ARCH.tar" "opsdesk-workforce-scoring_${VER}_$ARCH.tar"; do
  if [ ! -f "$DIR/$f" ] || [ "$(sha "$DIR/$f")" != "$(expected "$f")" ]; then
    [ -n "$RELEASE_DIR" ] && { echo "$DIR/$f is missing or does not match its SHA-256." >&2; exit 1; }
    echo "Downloading $f ..."
    curl -fL --retry 3 -o "$DIR/$f.part" "$BASE/$f"
    mv "$DIR/$f.part" "$DIR/$f"
  fi
  if [ "$(sha "$DIR/$f")" != "$(expected "$f")" ]; then
    rm -f "$DIR/$f"; echo "SHA-256 of $f does not match. Deleted it; run again." >&2; exit 1
  fi
  echo "$f: SHA-256 OK"
  docker load -i "$DIR/$f"
done

echo
echo "Demo: the demo request's reference calls (expect reward 1.0), then a run with no call (expect 0)."
sh demo/run_demo.sh
echo
echo "Done. Next: run your own agent on one of the 5 requests (README, \"Step by step\")."
