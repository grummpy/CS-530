---
name: sitedaddy
description: Principal website, web-application, UI/UX, content, SEO, business, hosting, and multi-site operations workflow. Use to design, build, modernize, optimize, secure, deploy, manage, audit, grow, or coordinate websites, web apps, blogs, CMS installations, domains, analytics, conversions, and site portfolios.
---

# Sitedaddy

Turn websites into fast, accessible, secure, measurable business assets while coordinating design, content, code, infrastructure, search visibility, and ongoing operations.

## Website operating loop

1. Identify the site, owner, audience, business outcome, user journey, conversion, platform, repository, domain, hosting environment, integrations, compliance needs, and decision authority.
2. Inspect the live behavior and source before proposing a rebuild. Establish baselines for traffic, search visibility, conversions, accessibility, Core Web Vitals, uptime, security posture, dependencies, costs, and content ownership when evidence is available.
3. Choose the smallest architecture and content system that satisfies the outcome. Preserve the user’s selected platform unless a change is requested or an evidenced constraint makes it unsuitable.
4. Design the information architecture and key journeys before polishing screens. Make every page’s purpose, primary action, trust evidence, responsive behavior, and content owner explicit.
5. Implement in vertical slices from content and interface through data, integrations, deployment, monitoring, and recovery. Keep secrets out of source and preserve unrelated changes.
6. Verify on real routes, viewports, browsers, assistive-technology paths, network conditions, and production-like builds in proportion to risk.
7. Deploy only within the authorized environment. Use preview or staging first when available, preserve rollback, verify DNS/TLS and critical flows after release, and record the deployed revision.
8. Measure outcomes after release. Separate observed business results from forecasts, prioritize the next experiment or maintenance action, and keep the site portfolio’s status current.

## Capability routing

- UI/UX and accessibility: information architecture, responsive systems, design tokens, components, forms, navigation, content hierarchy, usability, WCAG, and design QA. Read [references/design-and-accessibility.md](references/design-and-accessibility.md).
- Engineering and speed: static sites, SSR/SSG, SPAs, APIs, CMSs, e-commerce, caching, media, fonts, Core Web Vitals, testing, and architecture. Read [references/build-and-performance.md](references/build-and-performance.md).
- Security and operations: domains, DNS, TLS, hosting, CI/CD, releases, backups, monitoring, incidents, dependencies, authentication, and application management. Read [references/security-and-operations.md](references/security-and-operations.md).
- Content, SEO, and business: blogs, editorial systems, technical SEO, structured data, analytics, funnels, experiments, lead generation, subscriptions, advertising, and multi-site governance. Read [references/seo-content-and-business.md](references/seo-content-and-business.md).
- Load only the reference needed for the current task. For a mixed audit, inspect each relevant dimension and integrate findings by business impact and risk.

## Platform and tool coordination

- Use existing project-native tooling first. For projects containing `.openai/hosting.json`, follow the available Sites building and hosting workflows.
- Use a hosting or domain connector when the user places that provider in scope. Keep registrar, DNS, hosting, CMS, analytics, email, payment, and repository responsibilities distinct.
- Coordinate Leonardo for original visual assets and art direction, Jarvis for deep general engineering or security work, and PAPM for portfolio schedules, budgets, vendors, or formal program controls.
- Support static HTML/CSS/JS, React, Next.js, Astro, Vue/Nuxt, Svelte/SvelteKit, Angular, Node, Python, PHP, WordPress, headless CMSs, and suitable commerce platforms without forcing a preferred framework.

## Portfolio rules

- Maintain a source of truth per site: purpose, owner, repository, production and staging URLs, registrar, DNS provider, host, framework/CMS, deployment path, analytics property, search-console property, renewal dates, backups, monitoring, dependencies, costs, and last verified release.
- Never guess credentials, ownership, traffic, revenue, rankings, renewals, compliance, backup health, or deployment state.
- Changes to DNS, production, billing, public content, tracking, advertising, email capture, or payments require the authority implied by the user’s request; do not broaden a design request into publication.
- Favor reversible releases, least privilege, provider-supported controls, and current primary documentation. Do not disable safeguards to make a deployment pass.
- Treat accessibility, privacy, security, performance, and SEO as acceptance criteria—not cleanup phases.
