# Clay Fight Finishers

All finishers run only after a valid KO, lock simulation, are skippable, and use non-authoritative presentation frames. They end in exaggerated colored clay splats and confetti-gore rather than realistic injury.

| Winner | Setup | Target-specific punchline |
| --- | --- | --- |
| Rhinestone Angel | Five escalating star-guitar impacts | Each target gets a different final starburst color and prop silhouette. |
| Mr. President | An old rotary phone summons a toy-like jet flyover | The final burst uses kitchen, circuit, or star confetti to match the opponent. |
| Elon Gates | Wrist controller aligns satellite orbs | Each target is popped, toppled, or stomped into a clay puddle by a different orb pattern. |
| Master Chef | Kitchen Rush crosses knife and intact salmon | Each target gets a distinct comedic culinary sweep into a non-realistic clay splat. |

Runtime media lives in `assets/finishers/<winner>_vs_<loser>/frames/`; matching MP4 previews sit at `assets/finishers/<winner>_vs_<loser>.mp4`.

## Shot timing

All timelines use 30 frames at 10 fps (3 seconds): frames 0–5 establish the winner, 6–11 reveal the prop or call, 12–17 deliver the target-specific gag, 18–23 resolve to colored clay splat/confetti, and 24–29 hold a readable result. `Space` jumps to the hold frame and `R` resets the whole match.

| Winner | Opponent | Final gag |
| --- | --- | --- |
| Rhinestone Angel | Mr. President | Five guitar impacts end in an orange-and-navy star puddle. |
| Rhinestone Angel | Elon Gates | Five guitar impacts scatter teal circuitry confetti. |
| Rhinestone Angel | Master Chef | Five guitar impacts turn the kitchen props into star sprinkles. |
| Mr. President | Rhinestone Angel | Toy jets drop a gold-and-pink starburst payload. |
| Mr. President | Elon Gates | Toy jets drop a teal circuit confetti payload. |
| Mr. President | Master Chef | Toy jets drop a comic kitchen-scrap confetti payload. |
| Elon Gates | Rhinestone Angel | Satellite orbs create a star-token clay pop. |
| Elon Gates | Mr. President | Satellite orbs topple the target into an orange clay tumble. |
| Elon Gates | Master Chef | Satellite orbs stack into a stomp-shaped clay splat. |
| Master Chef | Rhinestone Angel | Knife-and-salmon sweep leaves a star-sprinkle clay splat. |
| Master Chef | Mr. President | Knife-and-salmon sweep leaves an executive-paper confetti splat. |
| Master Chef | Elon Gates | Knife-and-salmon sweep leaves a teal circuit confetti splat. |
