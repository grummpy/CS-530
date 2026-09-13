# G2: Data Pipeline and Vertical Slice Prompt

```text
Implement G2 only. Replace G1 hard-coded moves with versioned YAML or JSON content compiled into immutable typed definitions. Validate unique IDs, valid frame ranges, legal cancel targets, known animation/event references, valid box geometry, and bounded coordinates at startup and in tests.

Add one complete fighter package using the Captain Campaign prompt, one polished arena, a second graybox rival, and an arcade HUD. Implement locomotion, six normals, three command normals, three specials, throw, super, intro/outro, win/lose, and a non-graphic cinematic finisher. Keep all fighter differences in data or narrow reusable systems; do not add fighter-specific logic in the match loop.

Add presentation adapters for sprite animation, bounded two-fighter camera, event-driven audio, pooled VFX, and HUD. Presentation consumes deterministic events but cannot alter combat. Add a reusable finisher timeline: eligibility window, command gate, cinematic lock, deterministic timing, camera/VFX/audio event tracks, skip behavior in training, cleanup, and return to a valid round result. Test normal completion and skip with headless replay checksums.

Create a frame-data export and a replay viewer/tool stub. Measure cold launch, full-match FPS/frame time, and memory on the development machine; record measurements rather than assumptions. Update G2 evidence and stop.
```
