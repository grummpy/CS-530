# Sound Effects and Special Effects Prompt

```text
Create an original audio/VFX plan and placeholder implementation for a tactile clay fighter. Do not imitate a public figure’s voice, a known announcer, music, sound effect, or game audio.

Audio categories: UI select/back/pause; menu ambience; light/medium/heavy impact; block; throw; jump/land/dash; cloth/clay movement; whoosh; projectile; meter; super; finisher; win/lose; and arena ambience. Build light/medium/heavy impacts from original foley concepts such as thumb-pressed clay, rubber taps, cardboard bends, paper rustles, ceramic clicks, and soft drum hits. Use 3-5 variation pools with event IDs so replays never duplicate sounds during re-simulation. Route Master, Music, SFX, Voice, and UI mixer groups independently.

VFX categories: dust puff, clay crumb, paint splat, paper streamer, foam star, impact ring, speed line, block sparkle, meter flash, generic reaction bubble, and safe finisher burst. Use pooled sprite effects; VFX may react to simulation events but must never change gameplay. Keep effects readable, short, and bounded; respect reduced-screen-shake settings.

For each runtime asset include ID, source path, creator, original source method, license/ownership, duration, loop flag, loudness target, event trigger, variation group, and export format. Use placeholders only if clearly labeled. Every voiced line is an original fictional line; do not use celebrity-style performance direction.
```
