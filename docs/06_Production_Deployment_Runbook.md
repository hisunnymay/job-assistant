# AI Job Fit Assistant Deployment Runbook and Production Record

## Document Information

| Field | Value |
| --- | --- |
| Document | AI Job Fit Assistant Deployment Runbook and Production Record |
| Version | v1.0 |
| Status | Operational runbook |
| Owner | Mei Chang |
| Last updated | 2026-08-28 |
| Current production | `https://sunnydemo.me` on one Hong Kong server |
| Related files | [`compose.demo.yaml`](../compose.demo.yaml), [`compose.hk-production.yaml`](../compose.hk-production.yaml), [`deploy/nginx.hk-production.conf`](../deploy/nginx.hk-production.conf), [`deploy/release-candidate.json`](../deploy/release-candidate.json) |

## Version Log

| Version | Date | Change |
| --- | --- | --- |
| v1.0 | 2026-08-28 | Recorded the verified Hong Kong deployment and converted it into a reusable server/domain deployment procedure. |

> **Security rule:** Every value written as `<PLACEHOLDER>` must be supplied by the new operator. Never copy the real Ark key or PostgreSQL password from the current server into this report, Git, an image, a frontend build argument, a chat message, or logs.

---

## 1. Purpose and Scope

This document explains how the AI Job Fit Assistant was deployed and how to reproduce the same single-server production architecture on another Linux server or domain.

It covers:

- Preparing one Ubuntu server;
- Building immutable application images away from production;
- Transferring images and deployment-only files;
- Configuring PostgreSQL, FastAPI, React/Nginx, and Ark;
- Pointing a domain to the server;
- Issuing and automatically renewing a Let's Encrypt certificate;
- Starting, validating, backing up, updating, and rolling back production;
- Recording the actual `sunnydemo.me` deployment as a reference.

It does not purchase infrastructure, register or transfer a domain, submit an ICP filing, configure Ark account controls, or create application user accounts. Those are external account-owner actions.

The current production site is intentionally public without Basic Auth. The repository's base demo configuration still uses Basic Auth for local gateway testing; the production overlay must replace that mount and Nginx configuration.

---

## 2. Required Inputs

Collect these values before beginning:

| Placeholder | Example format | Purpose |
| --- | --- | --- |
| `<SSH_TARGET>` | `root@example-server` or an SSH alias | Server connection target |
| `<SERVER_IPV4>` | `203.0.113.10` | Public IPv4 address |
| `<DOMAIN>` | `app.example.com` | Production hostname |
| `<ADMIN_EMAIL>` | `ops@example.com` | Certificate-expiry notices |
| `<DEPLOY_ROOT>` | `/opt/job-assistant-production` | Root-only deployment directory |
| `<RELEASE_ID>` | `2026-08-28-01` | Immutable image label |
| `<POSTGRES_PASSWORD>` | Long random hexadecimal value | Database secret |
| `<ARK_API_KEY>` | Provider-issued secret | Ark authentication |
| `<ARK_MODEL>` | Approved Ark model identifier | Runtime model |
| `<BACKEND_IMAGE_ID>` | `sha256:...` | Loaded immutable backend image |
| `<GATEWAY_IMAGE_ID>` | `sha256:...` | Loaded immutable gateway image |
| `<YYYYMMDD-HHMMSS>` | `20260828-181500` | Explicit backup/release timestamp |

Required access and approvals:

- SSH access using a key, preferably as a non-root administrator with `sudo`;
- Cloud security-group or firewall access;
- DNS-zone access for the domain;
- Ark console access and an active model endpoint/key;
- Approval for the server/domain costs, production deployment, public exposure, and any paid Ark validation calls;
- A local machine or CI runner with Git, Docker Buildx, and the project source.

Generate the database password privately, for example with `openssl rand -hex 32`. Put the result directly into the server's protected environment file; do not commit it or include it in shell output captured by CI.

---

## 3. Deployment Architecture

```text
Recruiter browser
       |
       | DNS: <DOMAIN> -> <SERVER_IPV4>
       | HTTPS :443
       v
Nginx gateway container
       |-- /            -> React static files
       |-- /health      -> FastAPI health endpoint
       `-- /api/*       -> FastAPI backend container
                              |-- PostgreSQL container + persistent volume
                              `-- Volcengine Ark HTTPS API
```

All four services run on one Docker host:

- **Gateway:** public ports 80 and 443; TLS termination, redirect, static frontend, and API proxy;
- **Backend:** internal port 8000 only; business workflow, persistence coordination, and Ark integration;
- **Database:** internal port 5432 only; PostgreSQL persistent volume;
- **Ark:** external provider reached only by the backend.

Only SSH, HTTP, and HTTPS are exposed by the host. PostgreSQL and FastAPI are not published directly.

The base Compose project name is `job-assistant-demo`. Keep this name during migration or update because changing it creates a different Compose project and database-volume name.

---

## 4. Server Preparation

### 4.1 Recommended starting specification

The current MVP has run successfully on:

- Ubuntu 22.04 LTS, `x86_64`;
- 2 vCPU;
- Approximately 4 GB RAM;
- 40 GB system disk;
- Docker Engine and Docker Compose v2.

This is an observed MVP baseline, not a capacity guarantee. Monitor memory, disk, database growth, and traffic after release. Adding swap may improve resilience on a small host, but it does not replace sufficient RAM.

### 4.2 Cloud security group

Configure inbound rules before certificate issuance:

| Port | Protocol | Source | Use |
| --- | --- | --- | --- |
| 22 | TCP | Administrator IP/CIDR only | SSH administration |
| 80 | TCP | `0.0.0.0/0` and optional IPv6 equivalent | HTTP redirect and certificate validation |
| 443 | TCP | `0.0.0.0/0` and optional IPv6 equivalent | Public HTTPS site |

Do not open 5432 or 8000 publicly. If SSH is temporarily open more broadly, restrict it after confirming access from the administrator's fixed IP or VPN.

### 4.3 Install runtime packages

On Ubuntu 22.04, the current host uses the distribution packages `docker.io`, `docker-compose-v2`, and `certbot`:

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2 certbot
sudo systemctl enable --now docker

sudo docker --version
sudo docker compose version
sudo certbot --version
```

The production overlay uses Compose's `!override` tag. Docker Compose 2.40.3 is verified for this repository; validate the merged configuration before deployment if using another version.

### 4.4 Create the deployment directory

```bash
sudo install -d -m 700 <DEPLOY_ROOT>
sudo install -d -m 700 <DEPLOY_ROOT>/deploy
sudo install -d -m 700 <DEPLOY_ROOT>/backups
```

The current deployment runs from `/opt/job-assistant-production`. No project source is required on the production server—only prebuilt images, Compose files, Nginx configuration, renewal hooks, and the protected environment file.

### 4.5 Optional host firewall

Cloud security-group rules are mandatory. A host firewall is an additional layer. Before enabling UFW, allow the verified SSH path and keep the cloud console available to prevent lockout:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

Restrict the port 22 rule to the administrator's source CIDR when practical.

---

## 5. Domain and DNS Configuration

### 5.1 Create DNS records

In the authoritative DNS provider, create:

| Host | Type | Value | TTL |
| --- | --- | --- | --- |
| `@` for an apex domain, or the chosen subdomain | `A` | `<SERVER_IPV4>` | 600 seconds during rollout |
| `www` (optional) | `CNAME` | `<DOMAIN>` | 600 seconds during rollout |

If serving both apex and `www`, add both names to Nginx and the certificate. Otherwise configure only the hostname actually used by recruiters.

### 5.2 Verify delegation and propagation

From a network that is not using private or proxy DNS overrides:

```bash
dig +short NS <DOMAIN>
dig +short A <DOMAIN>
```

The `A` result must equal `<SERVER_IPV4>`. Check more than one public resolver if the record has just changed. Do not request the certificate until public DNS resolves correctly and inbound port 80 reaches the new server.

### 5.3 Verify the server address

On the server:

```bash
curl -4 https://ifconfig.me
```

Compare the returned address with the DNS `A` record and the cloud console's public IP.

---

## 6. Application Image Preparation

### 6.1 Validate the release locally

Normal automated validation remains provider-free unless a live Ark run is separately approved:

```bash
cd backend
uv sync --locked
AI_PROVIDER=mock uv run pytest
uv run mypy app tests
uv run ruff check .

cd ../frontend
npm ci
npm run test
npm run type-check
npm run lint
npm run build
npm run test:e2e
```

Return to the repository root before building images.

### 6.2 Build for the server architecture

The current server is `linux/amd64`. Build on the local machine or CI runner, even when the local machine is ARM:

```bash
docker buildx build \
  --platform linux/amd64 \
  --pull \
  --load \
  --file backend/Dockerfile.demo \
  --tag job-assistant-backend:<RELEASE_ID> \
  .

docker buildx build \
  --platform linux/amd64 \
  --pull \
  --load \
  --file frontend/Dockerfile.demo \
  --tag job-assistant-gateway:<RELEASE_ID> \
  .
```

The Dockerfiles use digest-pinned base images and locked dependency files. The gateway image contains the local protected-demo Nginx configuration, but production replaces it with a bind-mounted production configuration.

### 6.3 Record local image IDs

```bash
docker image inspect job-assistant-backend:<RELEASE_ID> --format '{{.Id}}'
docker image inspect job-assistant-gateway:<RELEASE_ID> --format '{{.Id}}'
```

Save these values in the release record. They must match the IDs loaded and run on the server.

### 6.4 Transfer the images

Create a bounded temporary directory rather than writing archives into the repository:

```bash
DEPLOY_ARCHIVE_DIR="$(mktemp -d)"

docker save \
  --output "${DEPLOY_ARCHIVE_DIR}/job-assistant-images.tar" \
  job-assistant-backend:<RELEASE_ID> \
  job-assistant-gateway:<RELEASE_ID>

gzip "${DEPLOY_ARCHIVE_DIR}/job-assistant-images.tar"
scp "${DEPLOY_ARCHIVE_DIR}/job-assistant-images.tar.gz" \
  <SSH_TARGET>:/tmp/job-assistant-images.tar.gz
```

Load on the server:

```bash
ssh <SSH_TARGET>
sudo gzip --decompress /tmp/job-assistant-images.tar.gz
sudo docker load --input /tmp/job-assistant-images.tar
sudo docker image inspect job-assistant-backend:<RELEASE_ID> --format '{{.Id}}'
sudo docker image inspect job-assistant-gateway:<RELEASE_ID> --format '{{.Id}}'
```

Compare the IDs with the local record. Remove the temporary archive only after the IDs match and the release is healthy. Do not build application source or edit a running container on the production server.

The PostgreSQL base is pinned by registry digest. Pull it before the first start:

```bash
sudo docker pull \
  postgres:16-alpine@sha256:cf78e76683b9ca8c5733cbbdce6c9262b45b6767934dd0a95e671f9a0fc20685
```

If the target server cannot reach that registry, pull the exact digest on the build machine and include it in the transferred `docker save` archive. Do not silently substitute an unpinned database image.

An approved private registry may replace this transfer process. In that case, use digest-qualified references such as `registry.example.com/app/backend@sha256:...` and verify the pulled digests.

---

## 7. Production Configuration

### 7.1 Files required on the server

Copy these deployment-only files into `<DEPLOY_ROOT>`:

```text
<DEPLOY_ROOT>/
├── compose.demo.yaml
├── compose.production.yaml
├── backups/
└── deploy/
    ├── demo.env
    ├── nginx.production.conf
    ├── start-production-gateway.sh
    └── stop-production-gateway.sh
```

Start from these repository files:

- [`compose.demo.yaml`](../compose.demo.yaml);
- [`compose.hk-production.yaml`](../compose.hk-production.yaml);
- [`deploy/nginx.hk-production.conf`](../deploy/nginx.hk-production.conf);
- [`deploy/start-hk-production-gateway.sh`](../deploy/start-hk-production-gateway.sh);
- [`deploy/stop-hk-production-gateway.sh`](../deploy/stop-hk-production-gateway.sh).

For another domain or path, copy the production-specific files to generic names and replace every `sunnydemo.me`, `/opt/job-assistant-production`, and `compose.hk-production.yaml` occurrence. Do not change the base file unless the application architecture itself changes.

### 7.2 Production Compose overlay

The production overlay must replace—not append to—the base gateway ports and volumes:

```yaml
services:
  backend:
    environment:
      FRONTEND_ORIGIN: https://<DOMAIN>

  gateway:
    ports: !override
      - "80:80"
      - "443:443"
    volumes: !override
      - ./deploy/nginx.production.conf:/etc/nginx/conf.d/default.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
```

`volumes: !override` is essential: it removes the base demo's Basic Auth password-file mount. Validate the merge before starting:

```bash
sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  config --quiet

sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  config
```

The rendered gateway must contain only the production Nginx and `/etc/letsencrypt` mounts.

### 7.3 Protected environment file

Create `<DEPLOY_ROOT>/deploy/demo.env` with mode `600` and the following keys:

```dotenv
POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
DEMO_PORT=80
POSTGRES_IMAGE=postgres:16-alpine@sha256:cf78e76683b9ca8c5733cbbdce6c9262b45b6767934dd0a95e671f9a0fc20685
BACKEND_IMAGE=<BACKEND_IMAGE_ID>
GATEWAY_IMAGE=<GATEWAY_IMAGE_ID>
AI_PROVIDER=ark
ARK_API_KEY=<ARK_API_KEY>
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_MODEL=<ARK_MODEL>
ARK_REQUEST_TIMEOUT_SECONDS=180
```

Use an editor that does not echo values into logs, then restrict the file:

```bash
sudo chmod 600 <DEPLOY_ROOT>/deploy/demo.env
sudo chown root:root <DEPLOY_ROOT>/deploy/demo.env
```

Do not include `DEMO_AUTH_FILE` in production. Do not pass `ARK_API_KEY` into the gateway image or frontend build. Use a long hexadecimal PostgreSQL password so it is safe inside the database URL assembled by Compose.

### 7.4 File permissions

```bash
sudo chmod 700 <DEPLOY_ROOT>
sudo chmod 600 <DEPLOY_ROOT>/deploy/demo.env
sudo chmod 644 <DEPLOY_ROOT>/deploy/nginx.production.conf
sudo chmod 700 <DEPLOY_ROOT>/deploy/start-production-gateway.sh
sudo chmod 700 <DEPLOY_ROOT>/deploy/stop-production-gateway.sh
```

---

## 8. Nginx Configuration

Create `<DEPLOY_ROOT>/deploy/nginx.production.conf`:

```nginx
server {
    listen 80;
    server_name <DOMAIN>;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name <DOMAIN>;

    ssl_certificate /etc/letsencrypt/live/<DOMAIN>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<DOMAIN>/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_session_timeout 1d;
    ssl_session_cache shared:TLS:10m;
    add_header Strict-Transport-Security "max-age=86400" always;

    location = /health {
        proxy_pass http://backend:8000/health;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_connect_timeout 10s;
        proxy_send_timeout 400s;
        proxy_read_timeout 400s;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
```

The 400-second gateway timeout covers at most two 180-second Ark attempts plus a finite margin. If the provider timeout or retry ceiling changes, update and revalidate the gateway timeout rather than making it unlimited.

The public production file must not contain `auth_basic` or `auth_basic_user_file`. Ark-side quotas can limit model spend, but they do not protect these public routes from repeated traffic.

---

## 9. HTTPS Certificate Setup

### 9.1 Issue the first certificate

Confirm that DNS resolves to the server and port 80 is free. The production gateway cannot start before the certificate files exist because Nginx mounts them at startup.

Recommended command with an operational contact email:

```bash
sudo certbot certonly \
  --standalone \
  --domain <DOMAIN> \
  --email <ADMIN_EMAIL> \
  --agree-tos \
  --no-eff-email
```

For both apex and `www`, add another `--domain` argument and update Nginx `server_name` accordingly.

Verify the certificate:

```bash
sudo openssl x509 \
  -in /etc/letsencrypt/live/<DOMAIN>/fullchain.pem \
  -noout -subject -issuer -enddate
```

### 9.2 Install renewal hooks

Certbot's standalone renewal temporarily needs port 80, so the pre-hook stops the gateway and the post-hook restores the exact production service without building.

The scripts must contain the real deployment root and production Compose filename:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd <DEPLOY_ROOT>
hook_log=/var/log/job-assistant-certbot-hook.log
docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  stop gateway >>"${hook_log}" 2>&1
```

The post-hook uses the same files with:

```bash
docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  up --detach --wait --no-build gateway >>"${hook_log}" 2>&1
```

Install them:

```bash
sudo install -m 700 \
  <DEPLOY_ROOT>/deploy/stop-production-gateway.sh \
  /etc/letsencrypt/renewal-hooks/pre/stop-job-assistant-gateway.sh

sudo install -m 700 \
  <DEPLOY_ROOT>/deploy/start-production-gateway.sh \
  /etc/letsencrypt/renewal-hooks/post/start-job-assistant-gateway.sh

sudo systemctl enable --now certbot.timer
```

After the application is running, rehearse renewal:

```bash
sudo certbot renew --dry-run --no-random-sleep-on-renew
sudo systemctl is-enabled certbot.timer
sudo systemctl is-active certbot.timer
```

Immediately recheck the public site after the rehearsal because the gateway is intentionally stopped and restarted.

---

## 10. Production Deployment Procedure

Because the current deployment root is mode `700` and root-owned, open a bounded root shell, enter the directory, perform the deployment/backup commands, and exit when finished:

```bash
sudo -i
cd <DEPLOY_ROOT>
```

The commands below assume that root shell. Keeping the directory root-only prevents other server users from reading the production environment or backups.

### 10.1 Preflight

```bash
sudo docker image inspect <BACKEND_IMAGE_ID> --format '{{.Id}}'
sudo docker image inspect <GATEWAY_IMAGE_ID> --format '{{.Id}}'

sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  config --quiet
```

Confirm before continuing:

- The environment file is `600` and not in Git;
- `FRONTEND_ORIGIN` exactly matches `https://<DOMAIN>`;
- Nginx certificate paths match `<DOMAIN>`;
- The effective gateway has ports 80/443 and no password-file mount;
- The certificate files exist;
- The image IDs match the approved release.

### 10.2 Start the stack

```bash
sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  up --detach --wait --no-build
```

`--no-build` prevents accidental source builds on production. The backend runs the idempotent database initialization before starting Uvicorn.

### 10.3 Inspect the running deployment

```bash
sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  ps

sudo docker inspect job-assistant-demo-backend-1 --format '{{.Image}}'
sudo docker inspect job-assistant-demo-gateway-1 --format '{{.Image}}'
sudo docker inspect job-assistant-demo-gateway-1 \
  --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'
sudo docker exec job-assistant-demo-gateway-1 nginx -t
```

Expected gateway mounts:

- `<DEPLOY_ROOT>/deploy/nginx.production.conf` to `/etc/nginx/conf.d/default.conf` read-only;
- `/etc/letsencrypt` to `/etc/letsencrypt` read-only.

There must be no `/etc/nginx/auth/demo.htpasswd` mount.

---

## 11. Database Setup and Recovery

Run the following database commands from `<DEPLOY_ROOT>` in the bounded root shell established in Section 10. This is required because shell output redirection to the root-only backup directory occurs before an individual `sudo` command would run.

### 11.1 Persistence

PostgreSQL stores data in the named Compose volume `demo_postgres`. `docker compose down` preserves it; `down --volumes` deletes it and must never be used on production unless permanent data removal is explicitly approved and a verified recovery path exists.

The application owns four public tables:

- `conversations`;
- `conversation_messages`;
- `feedback`;
- `user_behavior_events`.

### 11.2 Create a backup

Create a custom-format backup before every application/database change:

```bash
sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  exec -T database \
  pg_dump --username job_assistant --dbname job_assistant --format custom \
  > backups/pre-release-<YYYYMMDD-HHMMSS>.dump

sudo chmod 600 backups/pre-release-<YYYYMMDD-HHMMSS>.dump
```

Record the backup path and checksum:

```bash
sha256sum backups/pre-release-<YYYYMMDD-HHMMSS>.dump
```

Copy encrypted backups off the host according to the owner's retention policy. A backup stored only on the same server does not protect against total server loss.

### 11.3 Rehearse restore without touching production

```bash
sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  exec -T database \
  createdb --username job_assistant job_assistant_restore_test

sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  exec -T database \
  pg_restore \
    --username job_assistant \
    --dbname job_assistant_restore_test \
    --exit-on-error \
  < backups/pre-release-<YYYYMMDD-HHMMSS>.dump

sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  exec -T database \
  psql --username job_assistant --dbname job_assistant_restore_test \
  --command "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;"
```

After verification, remove only the disposable rehearsal database:

```bash
sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  exec -T database \
  dropdb --username job_assistant job_assistant_restore_test
```

Never copy production data into local development as a debugging shortcut.

---

## 12. Deployment Validation Checklist

### 12.1 Public checks that do not call Ark

```bash
curl --silent --show-error \
  --output /dev/null \
  --write-out 'status=%{http_code} redirect=%{redirect_url}\n' \
  http://<DOMAIN>/

curl --silent --show-error \
  --output /dev/null \
  --write-out 'status=%{http_code} tls=%{ssl_verify_result}\n' \
  https://<DOMAIN>/

curl --silent --show-error https://<DOMAIN>/health

curl --silent --show-error \
  --output /dev/null \
  --write-out 'status=%{http_code} type=%{content_type} bytes=%{size_download}\n' \
  https://<DOMAIN>/api/resume
```

Expected results:

- HTTP root: `301` to the same HTTPS hostname;
- HTTPS root: `200`, TLS verification result `0`;
- Health: `{"status":"ok"}`;
- Résumé: `200`, `application/pdf`, non-zero size.

### 12.2 Gateway and runtime checks

```bash
sudo docker exec job-assistant-demo-gateway-1 nginx -T 2>/dev/null \
  | grep auth_basic
```

For public production, this command must print nothing.

Also verify:

- Database and backend show healthy in `docker compose ps`;
- Running backend/gateway image IDs match the release record;
- Only 80/443 are published by Compose;
- `/health`, `/api/`, and `/` route to the intended targets;
- HSTS appears on the HTTPS response;
- No secret value appears in Git-tracked files, the frontend bundle, image history, or logs;
- Recent diagnostics do not print job descriptions, generated reports, raw provider responses, raw prompts, or authorization headers.

### 12.3 Ark workflow validation

The public checks above do not call Ark. A matching request and a follow-up are paid external actions and disclose the submitted job description to the configured provider. Run them only with explicit bounded approval.

Before production, use the protected local bundle and [`scripts/smoke-real-ai-demo.py`](../scripts/smoke-real-ai-demo.py) for the full matching/follow-up/replay/persistence/privacy smoke. It can use up to four provider attempts and expects local Basic Auth; it is not the public-production access check.

For production, perform the approved recruiter journey through the UI, confirm persistence and safe error behavior, and inspect only privacy-safe metadata. Do not print generated content into deployment logs.

### 12.4 Final sign-off evidence

Record:

- Deployment time and operator;
- Git commit/release identifier;
- Backend, gateway, and database image references;
- Database backup path and checksum;
- DNS result and server IP;
- Certificate subject and expiry;
- HTTP/HTTPS/health/résumé results;
- Container health;
- Whether a paid Ark smoke was approved and how many calls were used;
- Known limitations and rollback readiness.

---

## 13. Operations and Maintenance

### 13.1 Routine status and logs

```bash
cd <DEPLOY_ROOT>

sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  ps

sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  logs --since 30m backend gateway
```

Treat logs as sensitive operational data. Do not add debug logging that prints prompts, provider payloads, generated content, secrets, or recruiter-submitted content.

### 13.2 Restart without rebuilding

```bash
sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  up --detach --wait --no-build
```

### 13.3 Monitoring responsibilities

At minimum, monitor:

- Server subscription or trial expiry;
- TLS expiry and Certbot timer/hook failures;
- Free disk, memory, swap, container restarts, and database volume growth;
- PostgreSQL backup success and off-host restore rehearsal;
- Ark spend, token quotas, error rates, and model availability;
- Public request volume and repeated/error traffic;
- SSH login activity and security updates.

Ark constraints limit provider consumption but do not stop database growth, static traffic, or repeated API requests. If the audience expands, add application/gateway rate limiting and monitoring through a separately reviewed security change.

### 13.4 Security hardening

Recommended follow-ups:

- Use a dedicated administrative user and disable direct root SSH after testing;
- Restrict SSH to an administrator CIDR or VPN;
- Enable a host firewall after verifying console recovery access;
- Apply Ubuntu security updates on a controlled schedule;
- Add swap or increase memory if pressure appears;
- Register Certbot with a monitored email;
- Store encrypted backups off-host;
- Rotate Ark and PostgreSQL secrets after suspected exposure;
- Never expose ports 5432 or 8000 publicly.

---

## 14. Release and Rollback Procedure

### 14.1 Before every release

1. Validate the candidate locally with Mock AI and approved evaluation evidence.
2. Build immutable images for the server architecture.
3. Record the new image IDs/digests.
4. Record the currently running image IDs as the rollback target.
5. Create and rehearse a compatible PostgreSQL backup.
6. Transfer/load the new images without replacing running containers.
7. Update only the protected image-reference values in `deploy/demo.env`.

### 14.2 Deploy the new release

```bash
sudo docker compose \
  --env-file deploy/demo.env \
  --file compose.demo.yaml \
  --file compose.production.yaml \
  up --detach --wait --no-build
```

Run all non-provider public checks, then any separately approved paid workflow validation.

### 14.3 Application rollback

If the new release fails and the database remains compatible:

1. Restore `BACKEND_IMAGE` and `GATEWAY_IMAGE` in `deploy/demo.env` to the recorded preceding IDs/digests.
2. Run the same `up --detach --wait --no-build` command.
3. Verify running IDs, health, HTTPS, résumé, and the approved workflow.

If the database schema/data is incompatible, stop the application, restore the verified compatible backup under a written recovery plan, then start the preceding images. Never overwrite the production database merely to experiment.

The first production release has no preceding production application image. Its active image IDs and verified database backup establish the baseline; a full image rollback becomes testable after a second release exists.

---

## 15. Troubleshooting

| Symptom | Checks | Likely correction |
| --- | --- | --- |
| SSH fails | Cloud rule for port 22, correct key/user, server status | Restore source-CIDR rule or use cloud console; do not broadly reopen SSH permanently |
| Domain resolves incorrectly | Authoritative NS, `A` record, TTL/cache | Edit the authoritative zone and wait for propagation |
| Port 80/443 times out | Security group, UFW, `ss -ltnp`, Compose ports | Open required ports and confirm gateway is running |
| Certbot cannot validate | DNS target, port 80, another listener | Stop the gateway/other listener and retry standalone issuance |
| Nginx fails at startup | Certificate path, domain replacement, `nginx -t` | Correct the mounted config/certificate names; do not disable TLS validation |
| UI returns `401` | Effective mounts/config, `auth_basic` search | Confirm `volumes: !override` and mount the public production Nginx file |
| UI loads but API fails | `/api/` proxy, backend health, container network | Inspect privacy-safe gateway/backend logs and Compose health |
| `502 Bad Gateway` | Backend container status, internal port 8000 | Restore backend health; do not expose port 8000 publicly |
| Ark request times out | Backend/provider timeout, gateway 400s timeout, Ark status/quota | Check approved provider settings and bounded retries; keep timeouts finite |
| Database connection fails | Database health, password consistency, volume | Correct the protected environment and restart; do not print the password |
| Data disappears after redeploy | Compose project name/volume, accidental `down --volumes` | Restore the original project/volume or verified backup |
| Renewal succeeds but site stays down | Pre/post hook paths and Compose filenames | Correct hooks, run `bash -n`, rehearse renewal, and recheck HTTPS |
| Disk usage grows | Images, logs, backups, database volume | Retain required rollback assets, archive backups off-host, and remove only verified obsolete files |

---

## 16. Current Deployment Reference

The following was verified on 2026-08-28 and is a reference for reproducing—not copying secrets from—the current deployment.

### 16.1 Domain and server

| Item | Current value |
| --- | --- |
| Environment | Hong Kong production |
| Public URL | `https://sunnydemo.me` |
| Access | Public, no Basic Auth |
| Domain/DNS provider | Alibaba Cloud / HiChina DNS |
| Authoritative nameservers | `dns13.hichina.com`, `dns14.hichina.com` |
| Configured apex `A` target | `8.217.146.133` |
| Server public IPv4 | `8.217.146.133` |
| Server OS | Ubuntu 22.04.5 LTS, kernel 5.15, `x86_64` |
| Server capacity | 2 vCPU, approximately 3.5 GiB usable RAM, 40 GB root disk |
| Deployment root | `/opt/job-assistant-production` (`700`, root-owned) |
| Compose project | `job-assistant-demo` |
| Published ports | 80 and 443; SSH listens on 22 |

### 16.2 Runtime versions and images

| Item | Current value |
| --- | --- |
| Docker Engine | 29.1.3 |
| Docker Compose | 2.40.3 |
| Backend image ID | `sha256:1d0f83936f6d7d24dc81fe2ff1f2f712113caea9221f56e453898190a043c0fa` |
| Gateway image ID | `sha256:b54ba515917799658dea43e37db4e9e19011e106acbe2d8458c0ddc4ec14c3c1` |
| PostgreSQL image | `postgres:16-alpine@sha256:cf78e76683b9ca8c5733cbbdce6c9262b45b6767934dd0a95e671f9a0fc20685` |
| AI provider | Ark Responses-compatible path, configured server-side |
| Model | `doubao-seed-2-1-pro-260628` |
| Provider attempt timeout | 180 seconds |
| Gateway API timeout | 400 seconds |

### 16.3 TLS, backup, and validation

| Item | Current value |
| --- | --- |
| Certificate subject | `CN = sunnydemo.me` |
| Certificate issuer | Let's Encrypt |
| Certificate expiry | 2026-11-26 08:49:22 UTC |
| Renewal | Enabled/active Certbot timer with tested pre/post hooks |
| Environment file | `/opt/job-assistant-production/deploy/demo.env`, mode `600` |
| Baseline backup | `/opt/job-assistant-production/backups/initial-production.dump`, mode `600` |
| HTTP root | `301` to HTTPS |
| HTTPS root | `200`, valid TLS |
| Health | `200`, `{"status":"ok"}` |
| Résumé | `200`, PDF |
| Running auth directives/mount | None |

The remote Mock smoke and separately approved Ark smoke passed matching, follow-up, identical replay, persistence, privacy, and cleanup before Basic Auth was removed. The public-access conversion made no additional Ark call.

### 16.4 Known current limitations

- This is the first image set, so no preceding production image exists for rollback rehearsal;
- Ark/account constraints do not provide full public API abuse protection;
- Root SSH currently listens publicly and should be restricted at the cloud rule and host-policy levels;
- UFW is currently inactive;
- The server currently has no swap;
- Certbot was initially registered without a contact email;
- The Alibaba Cloud free-trial period shown during deployment ends on 2026-11-28;
- `/opt/job-assistant-staging` remains as an inactive root-only archive; its Basic Auth file was removed.

---

## 17. Reusable Deployment Checklist

### 17.1 Before deployment

- [ ] Hosting provider, region, specification, term, and cost approved;
- [ ] Public-access decision approved;
- [ ] Domain ownership and DNS-zone access confirmed;
- [ ] SSH key access works and port 22 is restricted;
- [ ] Ports 80 and 443 are open; 5432 and 8000 are closed publicly;
- [ ] DNS `A` record points to the server;
- [ ] Ark key/model access confirmed without exposing the key;
- [ ] Paid validation call ceiling approved if a live smoke is planned;
- [ ] Backend/frontend tests and release evidence pass;
- [ ] `linux/amd64` images built and IDs recorded;
- [ ] Production files contain the new domain and deployment path;
- [ ] Production environment file exists with mode `600` and no `DEMO_AUTH_FILE`;
- [ ] First Let's Encrypt certificate issued.

### 17.2 Deployment

- [ ] Image archives or registry digests transferred and verified;
- [ ] Compose merge passes `config --quiet`;
- [ ] Effective gateway mounts contain no auth password file;
- [ ] Database backup created and restore rehearsed;
- [ ] `up --detach --wait --no-build` succeeds;
- [ ] Database and backend are healthy;
- [ ] Running image IDs match the approved release;
- [ ] Nginx syntax passes;
- [ ] HTTP redirects to HTTPS;
- [ ] HTTPS, health, and résumé checks pass publicly;
- [ ] Certificate-renewal dry run restores the healthy gateway;
- [ ] Privacy-safe log inspection passes;
- [ ] Approved Ark recruiter journey passes, if authorized.

### 17.3 Final production sign-off

```text
Environment:
Domain:
Server provider/region:
Server public IP:
Deployment date/time:
Operator:
Release/Git identifier:
Backend image ID/digest:
Gateway image ID/digest:
Database image digest:
Preceding image IDs/digests:
Database backup path and SHA-256:
Certificate expiry:
Public validation result:
Ark validation approval/calls/result:
Known limitations:
Rollback decision and owner:
Server/certificate renewal owner:
```

Deployment is complete only when the live checks, recovery evidence, ownership, and known limitations are recorded. A healthy local build alone is release-candidate evidence, not proof that another domain/server is production-ready.
