#!/bin/zsh
# Run from the Desktop app bundle. Keep the playable checkout outside the app
# so updating it never changes the launcher itself.
set -euo pipefail

notify() {
  /usr/bin/osascript -e "display notification \"$1\" with title \"Papier Parade\"" >/dev/null 2>&1 || true
}
fail() {
  /usr/bin/osascript -e "display dialog \"Papier Parade could not start. Check your internet connection and Python 3.12 installation.\" buttons {\"OK\"} default button \"OK\" with title \"Papier Parade\"" >/dev/null 2>&1 || true
}
trap fail ERR

repo_url="https://github.com/grummpy/CS-530.git"
branch="grummpy-2d-game-orchestrator"
install_root="$HOME/Library/Application Support/Papier Parade"
checkout="$install_root/game"

mkdir -p "$install_root"
notify "Updating game…"
if [[ -d "$checkout/.git" ]]; then
  git -C "$checkout" fetch origin "$branch"
  git -C "$checkout" checkout "$branch"
  git -C "$checkout" pull --ff-only origin "$branch"
else
  git clone --branch "$branch" --single-branch "$repo_url" "$checkout"
fi

game_root="$checkout/projects/original-clay-fighter"
python_bin="${PYTHON_BIN:-/Users/daddy/miniconda3/bin/python3.12}"
if [[ ! -x "$python_bin" ]]; then
  python_bin="$(command -v python3.12 || true)"
fi
if [[ -z "$python_bin" ]]; then
  echo "Python 3.12 is required. Install it, then open Papier Parade again."
  exit 1
fi

if [[ ! -x "$game_root/.launcher-venv/bin/python" ]]; then
  "$python_bin" -m venv "$game_root/.launcher-venv"
fi
"$game_root/.launcher-venv/bin/python" -m pip install --quiet --upgrade pip
"$game_root/.launcher-venv/bin/python" -m pip install --quiet -e "$game_root"
cd "$game_root"
notify "Starting game…"
exec "$game_root/.launcher-venv/bin/python" -m fighter
