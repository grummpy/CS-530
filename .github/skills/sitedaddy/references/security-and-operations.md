# Security and operations

Use this reference for hardening, hosting, CI/CD, domains, application administration, monitoring, backup, and incident work.

## Threat and data boundaries

Identify public, authenticated, administrative, webhook, background-job, and third-party surfaces. Classify personal, payment, health, credential, and business-sensitive data. Define who can read, write, publish, deploy, administer, and recover each system.

Use maintained framework authentication and session facilities. Enforce authorization on the server for every protected object and action. Keep session identifiers out of URLs and logs; use secure cookie attributes and short, appropriate lifetimes. Protect state-changing browser requests against CSRF where the authentication model requires it.

## Hardened baseline

- HTTPS everywhere with automated certificate renewal; enable HSTS only after confirming every covered hostname supports HTTPS.
- Least-privilege credentials, MFA for administrators, separate human and machine identities, scoped secrets, rotation, and no credentials in source or browser bundles.
- Contextual output encoding, parameterized queries, input limits, safe file handling, SSRF controls, and explicit outbound destinations.
- Restrictive CORS, Content Security Policy, frame protections, MIME-sniffing protection, referrer policy, permissions policy, and appropriate cache controls.
- Rate limits and abuse controls on authentication, search, forms, uploads, APIs, email, and expensive operations.
- Dependency pinning, lockfiles, automated update review, vulnerability scanning, supported runtimes, and removal of unused plugins/themes/packages.

## Deployment and recovery

Use development, preview/staging, and production boundaries appropriate to the site. In GitHub Actions, protect production environments, restrict deployment branches, and scope environment secrets. Pin third-party actions to trusted immutable revisions when the project’s policy requires supply-chain hardening.

Every production release needs a known revision, reproducible build, migration plan, health check, critical-flow smoke test, observable logs/metrics, and rollback path. Backups are not proven until restore is tested. Record recovery point and recovery time objectives where downtime or data loss has business impact.

For DNS changes, capture current records and TTLs, validate the exact zone and target, stage low TTLs when justified, preserve mail and verification records, verify from authoritative and public resolvers, and allow for propagation. Never assume deleting a host also deletes its data safely.

## Multi-site operations

Maintain inventory and ownership. Monitor uptime, TLS expiry, domain renewal, backup freshness, error rate, failed jobs, storage, database health, dependency age, CMS/plugin updates, and broken critical journeys. Triage incidents by user impact and containment; preserve evidence and avoid destructive cleanup before recovery is understood.

## Authoritative sources

- OWASP Cheat Sheet Series: https://github.com/OWASP/CheatSheetSeries
- OWASP session management: https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Session_Management_Cheat_Sheet.md
- OWASP HTTP security headers: https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/HTTP_Headers_Cheat_Sheet.md
- GitHub deployment environments: https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments

For a security audit, use current framework advisories and deployment-provider documentation in addition to this baseline.
