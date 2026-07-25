---
title: Perspectives & Workloads
---

First deploy a sample app, then find it in the console.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/workloads
```

## Deploy an app to tour

Create a Deployment from the sample image. The `--image` flag names the image to run,
pulled from Harbor:

```terminal:execute
command: oc create deployment hello-dcs --image=${DCS_REGISTRY}/samples/hello-dcs:1.0
```

You should see `deployment.apps/hello-dcs created`.

Now wait until the app is running. `oc rollout status` watches the rollout and returns
once the Pod is ready; `--timeout=90s` makes it give up after 90 seconds rather than wait
forever:

```terminal:execute
command: oc rollout status deploy/hello-dcs --timeout=90s
```

```examiner:execute-test
name: verify-app-ready
title: Verify the app is running
timeout: 15
retries: .INF
delay: 2
```

## Open the Console tab

```dashboard:open-dashboard
name: Console
```

{{< note >}}
The real OpenShift console has two **perspectives** — **Developer** (app-centric, with a
visual Topology view) and **Administrator** (resource-centric). The project/namespace
selector matches your session namespace. _(screenshot: OpenShift console perspective
switcher + Topology view of hello-dcs.)_ The in-session Dashboard tab shows the same
underlying objects.
{{< /note >}}

## Workloads ↔ `oc`

**Workloads** in the console lists your Deployments and Pods — the same objects this
command shows. Switch back to the terminal and run it. The comma in `deploy,pods` asks for
two resource types at once, and `-l app=hello-dcs` filters by label so you see only this
app:

```terminal:execute
command: oc get deploy,pods -l app=hello-dcs
```

```examiner:execute-test
name: verify-workloads
title: Verify the workload is listed from the CLI
timeout: 10
retries: .INF
delay: 2
```

The same objects appear in two places. The console is useful for viewing topology and
status at a glance; the CLI is useful for making changes and for scripting.
