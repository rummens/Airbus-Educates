# From Docker to Kubernetes

**You already know Docker. This lab translates that knowledge onto DCS.**

You start from a real `docker-compose.yml` for the `hello-dcs` sample and migrate it one
object at a time.

The container becomes a **Deployment**. The `ports:` line becomes a **Service**. The
`environment:` block becomes a **ConfigMap**. Each step is applied and checked, so the app
is genuinely running when you finish.

Then you look at what is left over: four compose lines the platform refuses outright — and
which control rejects each one.

> **💡 Tip:** take this lab first if compose is still your mental model. The rest of the
> Build & Run track assumes the mapping this lab gives you.

- **Track:** Build & Run
- **Audience:** Intermediate — developers who run containers with Docker today
- **Duration:** ~25 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
- **Prerequisites:** the Core labs **Deploy Your First App** and **Configure & Troubleshoot Your App**. Nothing is carried over technically — this lab creates everything it needs.

## By the end of this lab you'll be able to

- Map the Docker and compose model onto Kubernetes objects: container → Pod/Deployment, `ports:` → Service, `environment:` → ConfigMap, `volumes:` → Volume.
- Explain the shift from **imperative** (`docker run`) to **declarative** (desired state the platform keeps true).
- Turn a compose service into a working Deployment, Service and ConfigMap on DCS.
- Name the four compose lines DCS rejects, and the platform control behind each.

## What you'll do

1. **Read** the compose file and the mapping table behind it.
2. **Translate** the container into a Deployment, with its image pulled from the DCS registry.
3. **Translate** the port mapping into a Service, and reach it by cluster DNS.
4. **Translate** the environment variable into a ConfigMap, and watch the rollout serve it.
5. **Face** the four lines that do not translate, and why the platform says no.

The last step is the one that changes how you build: the mapping is the easy half.
