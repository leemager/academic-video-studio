#!/bin/bash
# Mac bootstrap without Homebrew or a preinstalled Python.
set -euo pipefail
TASK_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$TASK_ROOT"
if [[ "$(uname -s)" != Darwin ]]; then
  printf '%s\n' 'This entry point is for macOS. On Windows/Linux use Python tools/bootstrap.py.' >&2
  exit 1
fi
if [[ "$(sysctl -in sysctl.proc_translated 2>/dev/null || true)" == 1 ]]; then
  exec /usr/bin/arch -arm64 /bin/bash "$0" "$@"
fi
case "$(uname -m)" in
  arm64) TASK_ARCH=aarch64 ;;
  x86_64) TASK_ARCH=x86_64 ;;
  *) printf '%s\n' 'Unsupported Mac architecture.' >&2; exit 1 ;;
esac
TASK_VERSION=0.8.22
TASK_STEM="uv-${TASK_ARCH}-apple-darwin"
TASK_NAME="${TASK_STEM}.tar.gz"
TASK_BASE="https://github.com/astral-sh/uv/releases/download/${TASK_VERSION}"
for TASK_DIR in .runtime .runtime/downloads .runtime/uv ".runtime/uv/${TASK_STEM}"; do
  if [[ -L "$TASK_DIR" ]]; then printf 'Refusing linked runtime directory: %s\n' "$TASK_DIR" >&2; exit 1; fi
  mkdir -p "$TASK_DIR"
done
TASK_ARCHIVE="${TASK_ROOT}/.runtime/downloads/${TASK_NAME}"
if [[ -L "$TASK_ARCHIVE" ]]; then printf '%s\n' 'Refusing linked archive.' >&2; exit 1; fi
if [[ ! -e "$TASK_ARCHIVE" ]]; then curl --fail --location --retry 2 "$TASK_BASE/$TASK_NAME" --output "$TASK_ARCHIVE"; fi
TASK_EXPECTED="$(curl --fail --silent --show-error --location "$TASK_BASE/$TASK_NAME.sha256" | awk 'NR==1 {print $1}')"
TASK_ACTUAL="$(shasum -a 256 "$TASK_ARCHIVE" | awk '{print $1}')"
if [[ "$TASK_EXPECTED" != "$TASK_ACTUAL" ]]; then printf '%s\n' 'Checksum failed. The archive is retained for diagnosis.' >&2; exit 1; fi
TASK_UV="${TASK_ROOT}/.runtime/uv/${TASK_STEM}/uv"
if [[ -L "$TASK_UV" ]]; then printf '%s\n' 'Refusing linked executable.' >&2; exit 1; fi
if [[ ! -e "$TASK_UV" ]]; then
  # Extract one known regular member to one bounded file; no archive paths are installed.
  tar -xzOf "$TASK_ARCHIVE" "$TASK_STEM/uv" > "$TASK_UV"
  chmod u+x "$TASK_UV"
fi
export UV_PYTHON_INSTALL_DIR="${TASK_ROOT}/.runtime/python"
export UV_PYTHON_BIN_DIR="${TASK_ROOT}/.runtime/python-bin"
export UV_CACHE_DIR="${TASK_ROOT}/.runtime/uv-cache"
"$TASK_UV" python install 3.11 --no-bin --no-registry
TASK_PYTHON="$("$TASK_UV" python find 3.11)"
exec "$TASK_PYTHON" tools/bootstrap.py "$@"
