---
title: Networking & Storage
---

Two more console sections, two more `oc` twins.

## Networking ↔ `oc`

The console's **Networking** area lists **Services** and **Routes** — the objects you
created in A04. _(screenshot: OpenShift console Routes list, with the external URL link.)_

The CLI equivalent lists the same, and works even when nothing's there yet:

```terminal:execute
command: oc get svc,route
```

```examiner:execute-test
name: verify-networking
title: Verify the Networking CLI view runs
timeout: 10
```

In the console you'd click a Route to open its external URL; from the CLI you read
`oc get route -o jsonpath='{.spec.host}'`. In A04 you did exactly that.

## Storage ↔ `oc`

The console's **Storage** area lists **PersistentVolumeClaims** with their storage class
and bound state — the PVC from A05. _(screenshot: OpenShift console PVC detail, showing
StorageClass and Bound status.)_

```terminal:execute
command: oc get pvc
```

```examiner:execute-test
name: verify-storage
title: Verify the Storage CLI view runs
timeout: 10
```

The console surfaces class and capacity visually; the CLI gives you the same in
`oc describe pvc`.
