#!/bin/bash
# No sudo or preinstalled Python needed; curl/tar/sha256sum are system prerequisites.
set -euo pipefail
TASK_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$TASK_ROOT"
[[ "$(uname -s)" == Linux ]] || { printf '%s\n' 'Use the entry point for your OS.' >&2; exit 1; }
case "$(uname -m)" in
  x86_64) TASK_ARCH=x86_64 ;;
  aarch64|arm64) TASK_ARCH=aarch64 ;;
  *) printf '%s\n' 'Unsupported Linux architecture.' >&2; exit 1 ;;
esac
TASK_VERSION=0.8.22
TASK_STEM="uv-${TASK_ARCH}-unknown-linux-gnu"
TASK_NAME="${TASK_STEM}.tar.gz"
TASK_BASE="https://github.com/astral-sh/uv/releases/download/${TASK_VERSION}"
for TASK_DIR in .runtime .runtime/downloads .runtime/uv ".runtime/uv/${TASK_STEM}"; do
  [[ ! -L "$TASK_DIR" ]] || { printf 'Refusing linked path: %s\n' "$TASK_DIR" >&2; exit 1; }
  mkdir -p "$TASK_DIR"
done
TASK_ARCHIVE="${TASK_ROOT}/.runtime/downloads/${TASK_NAME}"
[[ ! -L "$TASK_ARCHIVE" ]] || exit 1
if [[ ! -e "$TASK_ARCHIVE" ]]; then curl --fail --location --retry 2 "$TASK_BASE/$TASK_NAME" --output "$TASK_ARCHIVE"; fi
TASK_EXPECTED="$(curl --fail --silent --show-error --location "$TASK_BASE/$TASK_NAME.sha256" | awk 'NR==1 {print $1}')"
TASK_ACTUAL="$(sha256sum "$TASK_ARCHIVE" | awk '{print $1}')"
[[ "$TASK_EXPECTED" == "$TASK_ACTUAL" ]] || { printf '%s\n' 'Checksum failed; download retained.' >&2; exit 1; }
TASK_UV="${TASK_ROOT}/.runtime/uv/${TASK_STEM}/uv"
[[ ! -L "$TASK_UV" ]] || exit 1
if [[ ! -e "$TASK_UV" ]]; then tar -xzOf "$TASK_ARCHIVE" "$TASK_STEM/uv" > "$TASK_UV"; chmod u+x "$TASK_UV"; fi
export UV_PYTHON_INSTALL_DIR="${TASK_ROOT}/.runtime/python"
export UV_PYTHON_BIN_DIR="${TASK_ROOT}/.runtime/python-bin"
export UV_CACHE_DIR="${TASK_ROOT}/.runtime/uv-cache"
"$TASK_UV" python install 3.11 --no-bin --no-registry
TASK_PYTHON="$("$TASK_UV" python find 3.11)"
exec "$TASK_PYTHON" tools/bootstrap.py "$@"
