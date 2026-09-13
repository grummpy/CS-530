# G3 Finisher System Report

**Disposition:** implemented for the four-fighter roster.

The project contains twelve winner-versus-opponent finisher variants: 360 PNG runtime frames and twelve H.264 MP4 review videos at 640×360, 30 frames each. The app selects media only after a KO, locks the simulation through the existing phase gate, plays at 10 fps, supports Space skip, and keeps R reset available.

The visuals are deliberately exaggerated clay splats and colored confetti-gore. They are presentation-only: no frame, video, or skip action changes the winner, loser, KO, or rematch state.

Validation confirms every fighter has a timeline file, every directed matchup has 30 PNG frames and one decodable H.264 MP4, source compiles, and the media lookup resolves all twelve variants. Live window validation remains pending the configured Pygame-ce environment.
