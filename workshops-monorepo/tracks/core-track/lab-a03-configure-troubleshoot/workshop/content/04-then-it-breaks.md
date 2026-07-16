---
title: Then It Breaks
---

Config changes are also how apps break. Someone applies a manifest with a small mistake,
and suddenly the app won't start. Let's make that happen — on purpose — so you can learn
to deal with it calmly.

## Apply the broken version

`broken-deployment.yaml` is your configured app with **one** thing wrong. Apply it and
look at the Pods:

```terminal:execute
command: envsubst < broken-deployment.yaml | oc apply -f - && sleep 5 && oc get pods -l app=hello-dcs
```

You'll see a Pod that is **not** Ready — a status like `CreateContainerConfigError` (or a
Pod stuck not-ready). Something the new manifest asked for can't be satisfied.

```examiner:execute-test
name: verify-not-ready
title: Verify the app is currently broken (not ready)
timeout: 10
retries: .INF
delay: 2
```

{{< warning >}}
Don't fix anything yet. The next page is about *reading what the cluster is telling you* —
that skill matters more than the specific bug. Resist the urge to guess-and-poke.
{{< /warning >}}
