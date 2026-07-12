---
title: Summary
---

You saw the {{< param product_short >}} namespace model from both sides — not as a
diagram, but by creating a DEV and a PROD namespace and watching the same manifest be
accepted in one and rejected in the other.

## What You Did

- Learned **Namespace as a Service** — the namespace is the {{< param product_short >}} consumption unit.
- Created a **DEV** and a **PROD** namespace, distinguished by their type label.
- Deployed `hello-dcs` into DEV with no friction.
- Applied a **Kyverno** policy to PROD and watched it **reject** a non-compliant deploy.
- Learned why you **promote** compliant work into PROD rather than editing it in place.

## Challenge

Do it yourself, unguided: **get `hello-dcs` running in the `team-prod` namespace.** The
policy requires a `data-classification` label on the Deployment — make the manifest
compliant and apply it to PROD. When the app is running there, run the check.

```examiner:execute-test
name: verify-workload-ready
title: Challenge — hello-dcs promoted into PROD
args:
- hello-dcs
- team-prod
timeout: 90
retries: .INF
delay: 3
```

{{< note >}}
**Hint:** the policy message told you exactly what's missing — a `data-classification`
label on the Deployment's `metadata.labels`. Add one (any value, e.g. `internal`) and
apply the manifest into `team-prod`.
{{< /note >}}

{{< note >}}
**Reveal solution** — if you're stuck, run this:

```terminal:execute
command: |-
  oc apply -n team-prod -f - <<'EOF'
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: hello-dcs
    labels:
      app: hello-dcs
      data-classification: internal
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: hello-dcs
    template:
      metadata:
        labels:
          app: hello-dcs
      spec:
        containers:
        - name: hello-dcs
          image: ${DCS_REGISTRY}/samples/hello-dcs:1.0
          ports:
          - containerPort: 8080
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 100m
              memory: 64Mi
  EOF
```
{{< /note >}}

## Check Your Understanding

1. What is the concrete difference between a DEV and a PROD namespace on {{< param product_short >}}?

{{< note >}}
**Answer:** PROD namespaces enforce **Kyverno admission policies** (non-compliant
resources are rejected at apply time); DEV namespaces do not. Everything else — change
control, catalog access — follows from that "PROD is guarded" stance.
{{< /note >}}

2. Why have two namespace types at all?

{{< note >}}
**Answer:** So teams can iterate fast in DEV without ceremony, while PROD stays
controlled and repeatable. It separates "where you change things" from "where the real
thing runs."
{{< /note >}}

3. Your change needs to reach PROD. What's the right way to do it?

{{< note >}}
**Answer:** **Promote** it — make the manifest policy-compliant, review it, and apply the
tested version to PROD. You don't hand-edit what's already running in PROD.
{{< /note >}}

## Next Steps

Next in Foundations: **Working with Harbor**, the {{< param product_short >}} image
registry your workloads pull from.
