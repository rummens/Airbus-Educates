<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Deploy Your First App

The entry point to the course. You get your own app running on DCS in minutes, then look at how it works underneath.

Digital Container Service · DCS Academy

---

<!-- id: deploy -->
## Deploy it

- A **Deployment** tells DCS "keep one copy of this image running."
- It pulls the image from Harbor and starts a **Pod**.

```
oc create deployment hello-dcs \
  --image=${DCS_REGISTRY}/samples/hello-dcs:1.0
```

---

<!-- id: customise -->
## Customise it

- The app reads its greeting from an **environment variable**, `GREETING`.
- Setting an env var changes behaviour **without rebuilding the image**.

```
oc set env deploy/hello-dcs GREETING="Hello from the DCS Academy"
```

---

<!-- id: reach -->
## Reach it

- Nothing outside the cluster can reach the app yet.
- `oc port-forward` opens a **local tunnel** from your terminal to the Pod.
- A proper external address (a **Route**) comes in A03.

```
oc port-forward deploy/hello-dcs 8080:8080
curl -s localhost:8080
```

---

<!-- id: rollout -->
## Change it and watch the rollout

- Change the desired state, and the platform rolls out a **new Pod** with the new value.
- No downtime, nothing to restart by hand.

```
oc set env deploy/hello-dcs GREETING="Updated without a rebuild"
```

---

<!-- id: behind -->
## What's behind it

- **Imperative**: step-by-step commands — you did this with `oc create` / `oc set env`.
- **Declarative**: write down the desired state; the platform keeps reality matching it.
- Behind your commands sits one desired-state document:

```
Deployment  ->  ReplicaSet  ->  Pod
```

From A02 on, you write that document yourself.
