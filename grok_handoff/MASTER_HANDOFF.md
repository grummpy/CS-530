# Grok Master Build Prompt

```text
You are the lead implementation agent for this repository. Read these files before working:
1. docs/2D_FIGHTER_EXECUTIVE_PLAN.md
2. grok_handoff/README.md
3. every applicable prompt under grok_handoff/

Mission: build a local, two-player, original-fiction 2D clay-style fighting-game prototype that runs and debugs from PyCharm. Use Python 3.12+ and Pygame-ce. Follow the prompt sequence: G0 foundation, G1 graybox combat, G2 one polished vertical slice, G3 six-fighter roster alpha, then G4/G5 validation. Do not begin a later gate without recording acceptance evidence for the prior gate.

Hard content boundaries:
- Use only the six original fictional archetypes in grok_handoff/characters/. Do not use real people, likenesses, names, voices, biographies, catchphrases, political symbols, brands, signature clothing, or one-to-one event references.
- Do not reproduce source code, art, animation, UI, audio, dialogue, logos, stages, or trade dress from another game.
- No sexual content and no graphic or realistic violence. Finishers must use absurd clay deformation, paint, paper, confetti, toy props, or comic transformations.
- Do not add online networking, accounts, monetization, campaign mode, console certification, or more than six fighters.

Repository contract:
- Keep authoritative combat under src/fighter/sim/ and free of Pygame, rendering, audio, wall-clock time, and floating-point authoritative state.
- Store editable source art in art_source/, runtime exports in assets/, and data-defined moves/boxes/timelines in data/.
- Create and maintain docs/requirements_traceability.md, docs/asset_provenance.md, docs/originality_matrix.md, docs/content_review_log.md, docs/risk_decision_log.md, docs/balance_change_log.md, and docs/evidence/G0 through G5.
- Use small coherent commits. Do not commit credentials, virtual environments, caches, build output, or IDE-user state. Track large binary masters with Git LFS or document their external provenance.

At each gate, run the smallest relevant tests. Update requirement status and evidence with the exact tested commit SHA. Report scope completed, requirement/evidence table, changed files, validation results, content/originality review, risks/deferrals, and Gate Pass/Conditional pass/Blocked disposition.

After validation, push your committed work to the repository branch configured for this handoff:
git status
git add <only intended files>
git commit -m "<type>: <change> [REQ-ID]"
git push
Never force-push or rewrite shared history. If push fails because authentication or branch policy is unavailable, report the exact error and leave the local commit intact.
```
