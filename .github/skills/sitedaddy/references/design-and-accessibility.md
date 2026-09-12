# Design and accessibility

Use this reference for site strategy, UI systems, responsive design, UX reviews, forms, navigation, and accessibility.

## Start with journeys

Map audience → intent → entry page → decision information → primary action → confirmation → follow-up. Define failure, empty, loading, permission, offline, and recovery states for applications. For each important page, identify one primary action and the evidence needed to trust it.

Build information architecture from user vocabulary and task frequency. Use navigation labels that predict destinations. Keep critical information reachable without relying on hover, animation, color, or a specific viewport.

## Interface system

- Establish design tokens for color, type, spacing, radius, elevation, motion, breakpoints, and layer order; use semantic roles rather than page-specific values.
- Create components around behavior and meaning. Document variants, states, content limits, keyboard behavior, and responsive rules.
- Make layouts resilient to long names, localization, zoom, dynamic content, validation messages, reduced motion, and narrow screens.
- Use real content early. Placeholder copy hides hierarchy and wrapping failures.
- Preserve platform conventions for controls and input. Custom controls inherit responsibility for semantics, focus, keyboard behavior, and state announcements.

## Accessibility acceptance

Use the current applicable standard; WCAG 2.2 is the stable W3C recommendation at the time this reference was authored. Target level AA when the user has not supplied a stricter legal or organizational standard, but do not claim conformance from automated checks alone.

Verify at minimum:

- semantic headings, landmarks, labels, names, roles, values, and reading order;
- full keyboard operation, visible focus, logical focus movement, skip paths, and modal focus containment/return;
- text and non-text contrast, zoom/reflow, touch target size, orientation, and meaningful color independence;
- accessible errors, instructions, status announcements, time limits, authentication, and form completion;
- text alternatives, captions/transcripts where required, reduced motion, and no seizure-inducing content;
- screen-reader paths for each critical journey using at least one representative browser/reader pairing.

Automated scanners find only a subset. Combine linting and browser audits with keyboard, zoom, contrast, and assistive-technology evaluation.

## Design QA

Compare implementation against the design system at representative widths and content extremes. Check layout shift, clipping, overflow, focus indicators, hover/focus/active/disabled/error states, dark/light modes if supported, print behavior when relevant, and touch interactions on actual mobile hardware when practical.

## Authoritative sources

- W3C WCAG overview and current standard: https://www.w3.org/WAI/standards-guidelines/wcag/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WAI tutorials and testing resources: https://www.w3.org/WAI/tutorials/

Verify jurisdiction-specific accessibility obligations from current authoritative legal sources when the request is compliance-sensitive.
