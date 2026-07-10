---
title: Labels and Selectors
---

You've already been using `-l app=hello-dcs` to filter results. That works because of
**[labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)** —
key/value tags attached to resources — and **selectors**, which match on them. Labels are
one of the most important ideas in Kubernetes: they are how loosely-coupled pieces find
each other.

## Why Labels Matter

Kubernetes has no fixed hierarchy linking a Service to "its" Pods, or a Deployment to
"its" Pods. Instead, those links are made *dynamically* by matching labels:

- The Deployment's `spec.selector` says "I manage Pods labelled `app: hello-dcs`."
- Later, the Service's `spec.selector` will say "send my traffic to Pods labelled `app: hello-dcs`."

Any Pod that gains that label is automatically included; any that loses it drops out.
This is what makes scaling, rolling updates, and load-balancing work.

See the labels on your Pods:

```terminal:execute
command: oc get pods -l app=hello-dcs --show-labels
```

Expected — note the `app=hello-dcs` label (plus a `pod-template-hash` Kubernetes adds to
distinguish ReplicaSet generations):

```
NAME                         READY   STATUS    ...   LABELS
hello-dcs-6b8999855c-6jjhj   1/1     Running   ...   app=hello-dcs,pod-template-hash=6b8999855c
```

```examiner:execute-test
name: verify-labels
title: Verify pods carry the app label
args:
- hello-dcs
timeout: 10
```

## Querying by Label

Because labels are queryable, you can slice your resources any way you like. List just
the Pods for this app by name:

```terminal:execute
command: oc get pods -l app=hello-dcs -o name
```

You can combine labels (`-l app=hello-dcs,tier=frontend`), match many apps, or select
across resource types. As your project grows, disciplined labelling is what keeps it
navigable — adopt a consistent label scheme early.
