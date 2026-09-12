# Build and performance

Use this reference for architecture, implementation, modernization, testing, and speed work.

## Architecture choice

Decide from content change frequency, interactivity, personalization, authentication, SEO needs, data sensitivity, team skills, deployment target, uptime, and total operating cost.

- Prefer static delivery for content that can be built ahead of time.
- Add server rendering or edge rendering when request-time data or discovery requirements justify it.
- Use client-side rendering for interactions that genuinely benefit from it, not as a default for all content.
- Keep privileged logic and secrets server-side. Treat every browser input and client claim as untrusted.
- Prefer boring, supported dependencies over custom infrastructure unless a measured requirement demands otherwise.

## Performance budgets

Set page-type budgets before adding features: JavaScript, CSS, images, fonts, third-party requests, request count, server response, and Core Web Vitals. Measure production builds on representative mobile hardware and constrained networks.

Track current Core Web Vitals definitions and thresholds from web.dev. Use field data when available; lab tools diagnose but do not replace real-user evidence. Investigate LCP by phase, INP by interaction and main-thread work, and CLS by unstable elements. Do not optimize only a single Lighthouse score.

## Delivery tactics

- Serve correctly sized modern images with intrinsic dimensions; lazy-load offscreen media without delaying the likely LCP element.
- Subset and self-host fonts when justified, limit weights, preload only critical resources, and provide robust fallbacks.
- Remove unused client JavaScript, split by real route/feature boundaries, defer noncritical third parties, and avoid hydration when static HTML suffices.
- Cache immutable fingerprinted assets for a long duration; define deliberate caching and invalidation for HTML, APIs, and personalized data.
- Minimize redirect chains, blocking work, layout recalculation, and unbounded DOM growth.

## Verification stack

Use repository-native checks first, then add only needed coverage:

- formatting, linting, type checks, dependency checks, and unit tests;
- component and accessibility tests for reusable UI;
- integration tests for data boundaries and authorization;
- browser tests for critical user journeys and responsive behavior;
- production build, preview deployment, broken-link crawl, Lighthouse or equivalent audits, and target-host smoke tests.

Record URL, commit, build mode, device/profile, run count, and before/after results for performance claims. Keep screenshots or traces for material regressions.

## Authoritative sources

- Lighthouse source and documentation: https://github.com/GoogleChrome/lighthouse
- Core Web Vitals: https://web.dev/articles/vitals
- Web Platform Tests: https://github.com/web-platform-tests/wpt

Check framework and browser documentation for the exact versions in the project before applying version-specific commands.
