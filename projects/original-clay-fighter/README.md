# Papier Parade (subproject of CS-530)

Local two-player original-fiction 2D clay-style fighter.
Parent repo: [grummpy/CS-530](https://github.com/grummpy/CS-530).

This folder is the course home for the fighter. The separate
`grummpy/original-clay-fighter` repository is a satellite only.

## Status

Local workspace commit `d59b5b2`: G0–G5 plus local login screen,
placeholder foley, Blender atlas contract.

Full source currently lives in the Grok workspace
`original-clay-fighter/`. Copy or subtree-merge that tree here to
publish the complete act on CS-530.

```bash
# from a machine that has the full local tree
rsync -a --exclude .git original-clay-fighter/ CS-530/projects/original-clay-fighter/
cd CS-530
git add projects/original-clay-fighter
git commit -m "feat: add Papier Parade act under projects/"
git push
```
