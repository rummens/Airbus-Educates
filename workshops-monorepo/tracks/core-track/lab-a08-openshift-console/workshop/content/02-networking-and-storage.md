---
title: Networking & Storage
---

Two more console sections, two more `oc` twins.

## Networking ↔ `oc`

The console's **Networking** area lists **Services** and **Routes** — the objects you
created in A03. _(screenshot: OpenShift console Routes list, with the external URL link.)_

The CLI equivalent lists Services, and works even when nothing's there yet:

```terminal:execute
command: oc get svc
```

```examiner:execute-test
name: verify-networking
title: Verify the Networking CLI view runs
timeout: 10
```

Routes live here too — but creating and listing them needs the PROD-namespace access you
used in **A03** (`oc get route`, `oc get route -o jsonpath='{.spec.host}'`). This tour
namespace is DEV, so we list Services here.

## Storage ↔ `oc`

The console's **Storage** area lists **PersistentVolumeClaims** with their storage class
and bound state — the PVC from A04. _(screenshot: OpenShift console PVC detail, showing
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
