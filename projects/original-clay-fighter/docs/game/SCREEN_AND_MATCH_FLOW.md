# Screen and match flow

The playable shell uses the four shipped clay fighters: Rhinestone Angel, Mr.
President, The Tech Billionaire, and Master Chef. Existing fighter portraits,
animation frames, arena concept art, music, and finisher frames are used in the
game instead of substituting unrelated placeholder content.

## Title screen

The title screen presents all four fighters. Hovering a fighter plays frames
from that fighter's heavy-attack clip, raises the card, and displays the
fighter's short special-move slogan. The **START GAME** button responds to a
mouse click; Enter and Space also enter selection.

## Selection screen

Each card shows the fighter name, portrait, and satirical in-world slogan.
Click the upper half of a card to choose Player 1 and the lower half to choose
Player 2. Press `C` to toggle CPU control. CPU selection draws a seeded random
opponent from the other three fighters, and the bot approaches and chooses
attacks during the match. Select one of the three arena buttons, then activate
the **FIGHT!** button.

## Match HUD and controls

Every non-training round starts at 99 seconds. The top HUD contains each
fighter's health bar, a gold special meter, and the timer. Damage fills the
defender's special meter; at a full meter, the special button starts that
fighter's special sequence. Holding down (`S` for Player 1; Down Arrow for
Player 2) activates the blue shield ring and reduces incoming damage to one
third. A KO or timeout plays the appropriate winner-versus-opponent finisher
sequence; the fighter with more health wins a timeout.

| Player | Move | Block | Attacks |
| --- | --- | --- | --- |
| Player 1 | `A` / `D` | `S` | `F` light, `G` medium, `H` heavy, `J` special |
| Player 2 | Left / Right | Down | Keypad `1` light, `2` medium, `3` heavy, `0` special |

`R` resets the match and `Esc` exits the window.
