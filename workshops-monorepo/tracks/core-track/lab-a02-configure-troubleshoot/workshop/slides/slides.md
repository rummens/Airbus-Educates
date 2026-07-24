<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Configure & Troubleshoot Your App

Move configuration out of the command line and into dedicated objects — then break the app on purpose and learn to fix it.

Digital Container Service · DCS Academy

---

<!-- id: configmap -->
## Config in a ConfigMap

- A **ConfigMap** holds non-secret config as key/value pairs, outside the image.
- A Pod reads it two ways: as **environment variables** (`envFrom`) and as **files** (a volume mount).
- Same image, different ConfigMap per environment — no rebuild.

```
oc apply -f configmap.yaml
```

---

<!-- id: secret -->
## A Secret

- A **Secret** is like a ConfigMap, but for sensitive values (tokens, passwords).
- Values are **base64-encoded, not encrypted** — kept safe by RBAC, not by base64.
- Never print a Secret's value. Prove it is set by counting characters:

```
oc apply -f secret.yaml
oc exec deploy/hello-dcs -- printenv API_TOKEN | wc -c
```

---

<!-- id: rollout -->
## Roll out a change

- Editing a ConfigMap does **not** restart running Pods — a Pod reads its config only at start.
- Trigger a rollout so new Pods pick up the new value:

```
oc rollout restart deploy/hello-dcs
oc rollout status  deploy/hello-dcs --timeout=90s
```

---

<!-- id: breaks -->
## Then it breaks

- A small mistake in a manifest can stop the app from starting.
- Here you apply a broken Deployment on purpose.
- The Pod is **not Ready** — a status like `CreateContainerConfigError`.

```
oc get pods -l app=hello-dcs
```

---

<!-- id: diagnose -->
## Diagnose it

Read what the platform reports, in order — each command narrows the problem:

```
oc describe pod -l app=hello-dcs | tail -n 30
oc get events --sort-by=.lastTimestamp | tail -n 15
oc logs -l app=hello-dcs --tail=20
```

The events name the cause: a ConfigMap it references does not exist.

---

<!-- id: fix -->
## Fix it and verify

- Recover by re-applying the **known-good desired state** — the declarative way to recover.
- Then confirm the Pod is Ready again.

```
envsubst < deployment-configured.yaml | oc apply -f -
oc rollout status deploy/hello-dcs --timeout=90s
```

The loop: observe, diagnose, fix, verify.
