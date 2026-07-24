<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# What is DCS?

The one-glance version. Full detail is in the lab pages on the left — these slides are the map.

Digital Container Service · DCS Academy

---

<!-- id: platform -->
## An air-gapped, on-prem container platform

- Airbus Defence & Space's OpenShift-based platform.
- **Namespace as a Service** — you request namespaces and ship apps.
- **Air-gapped & sovereign** — everything comes from inside; images from Harbor.
- **Managed & self-service** — the platform team runs the clusters.

---

<!-- id: clusters -->
## Two clusters: Sandbox & PROD

- Essentially identical — same platform, same capabilities.
- One difference: **feature-rollout timing and maintenance / SLA**.
- New features land on Sandbox first, PROD about a month later.
- A cluster is **not** the same thing as a DEV/PROD namespace type.

---

<!-- id: images -->
## Images and containers

- An **image** is the built, read-only template of your app.
- A **container** is a running instance of that image.
- One image can start many containers at once.
- On DCS, images live in Harbor — you **pull**, you don't push.

---

<!-- id: kubernetes -->
## Why Kubernetes, not just Docker?

- **Scheduling** — the platform picks where your app runs.
- **Self-healing** — a crashed container comes back automatically.
- **Scaling** — ask for N copies, up or down.
- **Declarative** — describe the target; the platform keeps reality matching it.

Plain `docker run` does none of this on its own.

---

<!-- id: session -->
## Your session

- A browser terminal, already connected to DCS and your own project.
- Every command is run with `oc`, the OpenShift command line.
- Confirm who and where you are:

```
oc whoami
oc project -q
oc status
```

---

<!-- id: deploy -->
# Ready to deploy

That's the map. Head to **Deploy Your First App** to put it into practice — your own app running on DCS in minutes.
