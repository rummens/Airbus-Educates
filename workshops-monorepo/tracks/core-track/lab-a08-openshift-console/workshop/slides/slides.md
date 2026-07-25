<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# The OpenShift Console — A Guided Tour

Every action you did with `oc` in Core also has a visual equivalent in the web console. This lab finds those objects in the console and maps each view to the command you already know.

**In this lab:** perspectives and Workloads · Networking and Storage · Config · choosing the console or the CLI.

Digital Container Service · DCS Academy

---

<!-- id: workloads -->
## Perspectives & Workloads

The OpenShift console has two **perspectives**: **Developer** (app-centric, with a Topology view) and **Administrator** (resource-centric). The **Workloads** area lists your Deployments and Pods.

- Deploy a sample app first, then find it in the console.
- Workloads in the console shows the same objects as `oc get deploy,pods`.
- `-l app=hello-dcs` filters by label so you see only this app.
- Console is good for seeing status at a glance; the CLI is good for scripting.

```
oc create deployment hello-dcs \
  --image=${DCS_REGISTRY}/samples/hello-dcs:1.0
oc rollout status deploy/hello-dcs --timeout=90s
oc get deploy,pods -l app=hello-dcs
```

---

<!-- id: netstorage -->
## Networking & Storage

The console's **Networking** area lists **Services** and **Routes**; the **Storage** area lists **PersistentVolumeClaims** with their storage class and bound state.

- `oc get svc` lists Services and runs even when none exist yet.
- Routes need PROD-namespace access (A03); this tour namespace is DEV, so it lists Services only.
- `oc get pvc` lists the PersistentVolumeClaim from A04.
- The console shows class and capacity visually; `oc describe pvc` shows the same.

```
oc get svc
oc get pvc
```

---

<!-- id: config -->
## Config & When to Use Which

The console's **ConfigMaps** and **Secrets** views hold the configuration from A02. Secrets are shown masked in the UI, so a value is revealed only on purpose.

- `oc get configmap,secret` lists both in the terminal.
- Console: visual overview, one-off inspection, onboarding, exploring relationships.
- CLI: scripting, repeatable changes, bulk work, fast air-gapped operations.
- Same change across five namespaces in a pipeline: use the CLI.

```
oc get configmap,secret
```

---

<!-- id: next -->
## That's Core complete

You have now seen both sides of DCS: the `oc` command line and the web console that mirrors it.

- You found your app in Workloads, your Services in Networking, your PVC in Storage, and your ConfigMaps and Secrets in Config.
- You mapped each view to its `oc` equivalent and learned when to use which.

Pick a track next: **Developer** or **Security**.
