---
title: What's Behind It
---

You did all of that with imperative commands. Underneath, {{< param product_short >}}
turned every one of those into a single **desired-state document**. This page shows you
that document — it is the bridge to every later lab, where you write these documents
yourself.

*[📊 See this on a slide](/slides/#/behind) — opens the **Slides** tab on this topic.*

{{< note >}}
**Two ways to work: imperative and declarative.** These two words come up throughout the
course, so it is worth defining them plainly:

- **Imperative** means you give step-by-step commands — "create this", "set that". Each
  command does one thing, once. `oc create deployment` and `oc set env` are imperative.
- **Declarative** means you write down the end result you want — the *desired state* — in a
  file, and the platform makes reality match it and keeps it that way. The YAML you are
  about to see is declarative.

You just worked imperatively. From A02 on, you work declaratively.
{{< /note >}}

## Save and open the generated YAML

Save what `oc` generated, then open it in the editor:

```terminal:execute
command: oc get deploy hello-dcs -o yaml > deployment.yaml
```

```examiner:execute-test
name: verify-yaml-saved
title: Verify the Deployment YAML was saved
timeout: 10
```

```editor:open-file
file: ~/exercises/deployment.yaml
```

Three parts are worth finding:

- **`spec.replicas`** — how many copies you want (`1`). This is the number DCS keeps
  running; the "self-healing" you saw is DCS making reality match it.
- **`spec.selector.matchLabels`** — how the Deployment *finds* the Pods it owns
  (`app: hello-dcs`).
- **`spec.template.metadata.labels`** — the labels *stamped on* each Pod it creates. The
  selector and the template labels match — that's the glue.

## The ownership chain

The Deployment didn't create Pods directly. It created a
[**ReplicaSet**](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/),
and the ReplicaSet created the Pod. See all three at once:

```terminal:execute
command: oc get all -l app=hello-dcs
```

```examiner:execute-test
name: verify-ownership
title: Verify the Deployment → ReplicaSet → Pod chain
timeout: 10
```

**Deployment → ReplicaSet → Pod**, tied together by labels and selectors. Everything you
did by hand is captured in that YAML — and from A02 on, you'll write it directly instead
of generating it.
