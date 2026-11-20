#!/bin/sh
# One-command quick start: download the two images for this machine from the release, check them against the SHA-256
# values below, load them into Docker and run the demo (reference calls score 1.0, no call scores 0).
# Needs Docker, curl and about 250 MB of free disk. Images you already have locally: RELEASE_DIR=<folder> sh quickstart.sh
set -e
cd "$(dirname "$0")"
VER=3.12.5-sample-312en
BASE=https://github.com/vencur-ai/opsdesk-workforce-sample/releases/download/v3.12.5-sample

case "$(uname -m)" in
  x86_64|amd64) ARCH=amd64 ;;
  arm64|aarch64) ARCH=arm64 ;;
  *) echo "Unsupported machine: $(uname -m). Images exist for amd64 and arm64." >&2; exit 1 ;;
esac
command -v docker >/dev/null 2>&1 || { echo "Docker is needed: https://docs.docker.com/get-docker/" >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "Docker is installed but not running. Start it and try again." >&2; exit 1; }

expected() {  # SHA-256 of each release image (the same values as SHA256SUMS_RELEASE on the release page)
  case "$1" in
    opsdesk-workforce_${VER}_amd64.tar)         echo 79f4a26d02c24da55d162039dc03d55e6488e5595d9ac8053ee46baeb0d48403 ;;
    opsdesk-workforce-scoring_${VER}_amd64.tar) echo 1e5a11a2f4d727cfea55b11b8d4328b1829e69bc85f0e169eae17cf5acf6bd9a ;;
    opsdesk-workforce_${VER}_arm64.tar)         echo 657dac98e9436f142cce6e417096a24e1b6dae2c1a1b07a7cbc9045c873e2756 ;;
    opsdesk-workforce-scoring_${VER}_arm64.tar) echo e2f4f828e17f937cf786b2ce756022d5a21521244d4e74c204b9bbaa2c4fc3b3 ;;
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
