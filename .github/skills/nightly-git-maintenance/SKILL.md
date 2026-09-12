# Nightly Git Maintenance

Run this procedure at 2:00 AM local time for the active project session.

1. Inspect `git status --short`, the current branch, remote tracking, and the complete diff.
2. Do not add credentials, environment files, local virtual environments, build artifacts, or unrelated generated files. If a change may contain a secret or cannot be safely understood, leave it uncommitted and report the blocker.
3. Stage the remaining project changes, create a clear conventional commit with the required Copilot co-author trailer, and push the current branch to its configured upstream. Do not force-push, amend, rebase, or overwrite remote history.
4. Confirm the push succeeded and that the working tree is clean. Report any rejected push, merge conflict, authentication failure, or uncommitted unsafe file explicitly.
5. Inspect project sessions. Archive only child sessions that are verified completed, have no pending changes, no open pull request, no running automation, and no remaining work. Never archive active sessions, current sessions, open pull-request sessions, or user chats.
6. Never manually delete Copilot session event history, workspace metadata, lock files, or directories. Archiving eligible completed sessions is the supported, reversible cleanup operation.

If there is nothing safe to commit or archive, report that the maintenance check completed without changes.
