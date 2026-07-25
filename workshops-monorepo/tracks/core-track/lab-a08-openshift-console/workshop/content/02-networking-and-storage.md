---
title: Networking & Storage
---

Two more console sections, each with a matching `oc` command.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/netstorage
```

## Networking ↔ `oc`

The console's **Networking** area lists **Services** and **Routes** — the objects you
created in A03. _(screenshot: OpenShift console Routes list, with the external URL link.)_

The matching CLI command lists Services, and runs even when none exist yet:

```terminal:execute
command: oc get svc
```

```examiner:execute-test
name: verify-networking
title: Verify the Networking CLI view runs
timeout: 10
```

Routes are listed here too, but creating and listing them needs the PROD-namespace access
you used in **A03** (`oc get route`, `oc get route -o jsonpath='{.spec.host}'`). This tour
namespace is DEV, so here we list Services only.

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

The console shows the storage class and capacity visually; `oc describe pvc` shows the
same details in the terminal.
