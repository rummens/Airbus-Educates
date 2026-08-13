# From Docker to Kubernetes on DCS

**You already know Docker — this lab teaches you the translation reflex onto DCS.**

If you run apps with `docker run` or `docker-compose up` today, Kubernetes doesn't
replace what you know — it renames and restructures it. This lab takes a small
docker-compose file and migrates it, object by object, into a Deployment, a
Service and a ConfigMap on DCS. Then it walks the lines in that compose file that
*don't* survive the trip — a privileged container, a host bind mount, a root user,
a `latest`-tagged Docker Hub image — and explains exactly why DCS rejects each one.

- **Track:** Developer — Build on DCS · Lab 1
- **Audience:** Intermediate — comfortable with Docker/docker-compose; done the Core track (especially A01, A02)
- **Duration:** ~25 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** lab-a01-deploy-first-app; lab-a02-configure-troubleshoot — comfortable with `docker run` / `docker-compose.yml`

## By the end of this lab you'll be able to

- Map `docker run` / docker-compose concepts to their Kubernetes equivalents — container → Pod/Deployment, `-p`/`ports` → Service, `-e`/`environment` → ConfigMap, `-v` → Volume.
- Turn a docker-compose service definition into an equivalent Deployment + Service + ConfigMap and deploy it.
- Identify what does **not** translate on DCS and why: `privileged`/host mounts, the `latest` tag, running as root, and images from outside Harbor.
- Confirm the migrated app runs "the Kubernetes way" — self-healing, declarative, reachable by a stable name.

## What you'll do

Starting from a `docker-compose.yml` for the `hello-dcs` sample, you'll fill in and
apply a Deployment (the container), a Service (the port mapping), and a ConfigMap
(the environment variable) — then read through the compose file's four
unportable lines and see exactly which DCS control rejects each one.
