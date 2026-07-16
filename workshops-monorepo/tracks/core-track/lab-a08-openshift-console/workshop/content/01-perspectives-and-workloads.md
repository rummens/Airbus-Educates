---
title: Perspectives & Workloads
---

Let's get something on screen to look at, then find it in the console.

## Deploy an app to tour

```terminal:execute
command: oc create deployment hello-dcs --image=${DCS_REGISTRY}/samples/hello-dcs:1.0 && oc rollout status deploy/hello-dcs --timeout=90s
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

**Workloads** in the console lists your Deployments and Pods — the same thing this command
shows. Switch back to the terminal and run:

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

Same objects, two views. The console is great for *seeing* topology and status at a
glance; the CLI is great for *doing* and scripting.
