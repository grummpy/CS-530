# macOS launcher

## Download

Download [Papier-Parade-macOS-Launcher.zip](Papier-Parade-macOS-Launcher.zip),
unzip it, and move **Papier Parade.app** to Applications or the Desktop. On
first open, macOS may require you to approve the app because it is an unsigned
personal-project launcher. The app fetches the playable game branch from this
repository, creates its local Python environment, and starts the game.

To recreate the archive from source, run `build_desktop_launcher.sh` on a Mac,
then archive the generated `Papier Parade.app` with `ditto -c -k --keepParent`.

SHA-256 for the current archive:

`e147afb22f3a8a76a0ccc5f827d19dea62222f01fae361bd25a0d49576a4c43e`

`build_desktop_launcher.sh` creates **Papier Parade.app** on the current
user's Desktop. Its bundled Tech Billionaire cover image identifies the app.
When opened, the launcher updates the dedicated checkout in
`~/Library/Application Support/Papier Parade/game`, creates or refreshes its
Python 3.12 virtual environment, and starts the Pygame game.

The launcher follows the `grummpy-2d-game-orchestrator` branch because that is
the current playable GitHub release branch. It uses a fast-forward-only pull,
so a local edit in the managed checkout never gets overwritten silently.
