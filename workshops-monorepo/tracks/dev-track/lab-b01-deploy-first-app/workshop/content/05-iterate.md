---
title: Iterate
---

You have a running, reachable app. Real development is a **loop**: change something, roll it
out, verify. Let's run that loop once — the same moves you'll use every day on
**{{< param product_name >}}**.

## Scale it

Right now one Pod serves the app. Ask for two:

```terminal:execute
command: oc scale deployment/hello-dcs --replicas=2
```

Watch them arrive in a split terminal:

```terminal:execute
command: oc get pods -l app=hello-dcs -w
session: 2
```

Expected: a second `hello-dcs-…` Pod appears and reaches `Running` / `1/1`. Both Pods sit
behind the same Service — the Service now load-balances across both (its selector
`app: hello-dcs` matched the new Pod automatically).

Confirm two replicas are ready:

```examiner:execute-test
name: verify-replicas
title: Deployment scaled to 2 ready replicas
args:
- hello-dcs
- "2"
timeout: 5
retries: 5
delay: 2
```

Stop the watch with `Ctrl-C` in the lower terminal.

## Roll out a change

Deployments update **without downtime** — a new ReplicaSet is created and Pods are replaced
gradually. In a real change you'd bump the image tag in `deployment.yaml` and re-apply; here,
trigger a rollout so you can watch the mechanics:

```terminal:execute
command: oc rollout restart deployment/hello-dcs
```

```terminal:execute
command: oc rollout status deployment/hello-dcs
```

Expected: `deployment "hello-dcs" successfully rolled out`. Old Pods are drained as new ones
become Ready — the Service only ever routes to Ready Pods, so the app stays up.

{{< note >}}
This is the developer **inner loop**: edit a manifest → `oc apply` → `oc rollout status` →
verify. The image itself always comes from Harbor (`{{< param dcs_registry >}}`) — you change
*what runs*, never *where the image comes from*.
{{< /note >}}
