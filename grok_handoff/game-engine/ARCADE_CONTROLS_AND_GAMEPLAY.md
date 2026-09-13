# Arcade Controls, UI Overlay, and Play Contract

```text
Design the game for a six-button arcade layout while retaining keyboard/controller parity:

     [L] [M] [H]
     [S] [T] [Start]

L/M/H are light, medium, and heavy attacks. S is special, T is throw, and Start pauses/confirms. The lever/D-pad uses eight physical directions but combat normalizes directions to facing-relative inputs. Display this layout in the character-select/tutorial UI using original molded-plastic button icons, never cabinet art or labels copied from another game.

Universal mechanics: walk, crouch, jump, forward/back dash, high/low block, throw, light/medium/heavy normals, special motion commands, meter gain/spend, hitstop, launch, knockdown, recovery, super, and a gated round-end finisher. Keep the first prototype to a readable four-to-six action vocabulary and avoid assists, tags, air dashes, or advanced systems until proven by playtest.

Training mode must show current/previous input, facing-relative command buffer, health/meter reset, dummy state, fighter state/move/frame, and hit/hurt/push boxes. Acceptance: a new player can find controls and play a round; an advanced player can reproduce a command and diagnose its frame data.
```
