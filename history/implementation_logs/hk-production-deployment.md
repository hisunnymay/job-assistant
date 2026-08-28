# Hong Kong Production Deployment

## Status

The approved Hong Kong recruiter-production environment is live at `https://sunnydemo.me`. The UI and API are intentionally public without Basic Auth. The Ark-enabled backend and PostgreSQL persistence remain active behind the HTTPS gateway.

## Material Changes

- Added `compose.hk-production.yaml` to layer the `sunnydemo.me` origin, public HTTP/HTTPS ports, production Nginx configuration, and read-only Let's Encrypt certificate mount over the approved base Compose bundle while overriding the base Basic Auth mount.
- Added `deploy/nginx.hk-production.conf` with HTTP-to-HTTPS redirect, TLS 1.2/1.3, one-day HSTS, the existing single-origin proxy routes, and the approved finite 400-second AI gateway timeout without authentication directives.
- Added Certbot pre/post hooks that stop the production gateway for standalone HTTP-01 renewal and restore the exact no-build Compose service afterward.
- Created `/opt/job-assistant-production`, copied the verified database backup, transferred only immutable `linux/amd64` images and deployment files, and loaded no repository source on the server.
- Kept the running backend and gateway pinned to content IDs `sha256:1d0f83936f6d7d24dc81fe2ff1f2f712113caea9221f56e453898190a043c0fa` and `sha256:b54ba515917799658dea43e37db4e9e19011e106acbe2d8458c0ddc4ec14c3c1`. PostgreSQL remains pinned to the approved registry digest.
- Removed the generated Basic Auth password and hash files locally and from the retired staging deployment. Ark and PostgreSQL secrets remain only in ignored local files and mode-restricted server configuration.
- Updated Backend Technical Design v1.1, PLAN v0.43, the release manifest, tests, and README to designate Hong Kong as current production and distinguish the public production overlay from the protected local demo harness.

## Validation

- `http://sunnydemo.me` redirects to HTTPS; the public HTTPS UI, `/health`, and `/api/resume` return `200` without credentials; HSTS is present and the résumé response remains a PDF.
- The running production gateway has no `auth_basic` directive and no password-file mount.
- PostgreSQL, backend, and gateway containers are healthy after the overlay switch and after the certificate-renewal rehearsal.
- The Let's Encrypt certificate for `sunnydemo.me` is valid through 2026-11-26. The enabled Certbot timer and renamed production pre/post hooks passed a no-random-delay renewal dry run.
- The active application image content IDs match the approved transferred images. Nginx configuration syntax passed.
- Existing production persistence remained intact. Recent backend/gateway logs contained none of the checked Ark-key, authorization, submitted-description, raw-provider-response, or system-prompt markers.
- The earlier bounded remote Mock and separately approved four-call Ark gateway smokes passed matching, follow-up, replay, persistence, privacy, and cleanup before public authentication was removed. No additional Ark call was made for the access change.
- The custom PostgreSQL backup is retained at `/opt/job-assistant-production/backups/initial-production.dump`; the preceding restore rehearsal recovered all four public tables in a disposable database.

## Remaining Limitations

- This is the first production application image set, so no preceding production image exists to exercise as a rollback target. The active content IDs and verified database backup establish the baseline for the next release.
- Ark-side quotas or rate limits can bound model spend but do not prevent repeated public API requests, database growth, or non-AI traffic. The user accepted the current public-access risk and plans to configure Ark constraints; application/gateway abuse controls remain follow-up work if exposure broadens.
- The ECS host currently permits root SSH from any IPv4 source through its existing security-group rule, host UFW is inactive, and the server has no swap. These pre-existing host-hardening items remain pending.
- Certbot was registered without a contact email, so certificate-expiry email alerts are unavailable even though automated renewal is enabled and tested.
- The Alibaba Cloud free-trial period shown during deployment ends on 2026-11-28.
- The old `/opt/job-assistant-staging` directory is inactive and retained temporarily as a root-only deployment archive; its Basic Auth file was removed. Production runs only from `/opt/job-assistant-production`.

## Conformance

- Public APIs, frontend behavior, persistence ownership, AI Service boundaries, strict schemas/invariants, two-attempt ceiling, fixed résumé resources, and non-streaming behavior are unchanged.
- The user explicitly approved designating Hong Kong as production, making the site public, activating Ark, and the bounded paid validation that was already completed.
- No source build or source edit occurred on the server. No commit, push, merge, pull request, mainland deployment, additional provider call, or new purchase was performed during the public production conversion.
