# macOS launcher

`build_desktop_launcher.sh` creates **Papier Parade.app** on the current
user's Desktop. Its bundled Tech Billionaire cover image identifies the app.
When opened, the launcher updates the dedicated checkout in
`~/Library/Application Support/Papier Parade/game`, creates or refreshes its
Python 3.12 virtual environment, and starts the Pygame game.

The launcher follows the `grummpy-2d-game-orchestrator` branch because that is
the current playable GitHub release branch. It uses a fast-forward-only pull,
so a local edit in the managed checkout never gets overwritten silently.
