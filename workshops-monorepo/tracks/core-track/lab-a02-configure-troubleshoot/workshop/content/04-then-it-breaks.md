---
title: Then It Breaks
---

Config changes are also a common way for apps to break. Someone applies a manifest with a
small mistake, and the app no longer starts. This page introduces such a mistake
deliberately, so the next pages can teach you how to find and fix it.

*[📊 See this on a slide](/slides/#/breaks) — opens the **Slides** tab on this topic.*

## Apply the broken version

`broken-deployment.yaml` is your configured app with **one** thing wrong. Apply it, the
same two-step way as before:

```terminal:execute
command: envsubst < broken-deployment.yaml | oc apply -f -
```

Now list the Pods for this app to see the result:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

The `-l app=hello-dcs` flag filters the list to Pods with that label, so you see only this
app. You'll see a Pod that is **not** Ready — a status like `CreateContainerConfigError`
(or a Pod that stays not-ready). Something the new manifest asked for cannot be satisfied.

```examiner:execute-test
name: verify-not-ready
title: Verify the app is currently broken (not ready)
timeout: 10
retries: .INF
delay: 2
```

{{< warning >}}
Don't fix anything yet. The next page is about *reading what the cluster is telling you* —
that skill matters more than this specific bug. Try to diagnose the cause from the
cluster's own messages before changing anything.
{{< /warning >}}
