---
title: Persistence and Classification
---

Now the payoff — and two {{< param product_short >}}-specific things you must know about
choosing and obtaining storage.

## Prove it survives a restart

Delete the running Pod. The Deployment will immediately create a replacement:

```terminal:execute
command: oc delete pod -l app=hello-dcs
```

{{< note >}}
The Deployment starts a fresh Pod — give it a few seconds to be Running again.
{{< /note >}}

```examiner:execute-test
name: verify-pods-running
title: A fresh pod is running after the restart
args:
- hello-dcs
- "1"
timeout: 120
retries: .INF
delay: 3
```

The new Pod is a brand-new container — its own filesystem is empty. But it mounted the *same
PVC*, so read the marker back:

```terminal:execute
command: oc exec deployment/hello-dcs -- cat /data/marker
```

```examiner:execute-test
name: verify-marker
title: The data survived the pod restart
args:
- hello-dcs
- /data/marker
- persisted-by-dcs
timeout: 15
retries: 5
delay: 3
```

The file is still there. That's the whole point of persistent storage: the data lives in the
PV, not the Pod, so it outlives any single container.

## Classification drives the class

On {{< param product_short >}}, choosing a storage class isn't only about File vs Block or
performance — it's a **compliance** decision. As a multi-national platform (e.g. Germany and
Spain), {{< param product_short >}} ties storage to **data classification** and residency:
data of a given classification may only live on a storage class approved for it. Pick the
wrong class and you're not just slower — you may be **out of compliance**. When you provision
real storage, check your data's classification against the approved classes; see the
[{{< param product_short >}} storage documentation]({{< param dcs_docs_base_url >}}/concepts/storage).

## Object (S3) storage is a ticket

File and Block come through a PVC, self-service. **Object storage (S3)** does **not** — there
is no S3 storage class to claim. You obtain an S3 bucket by raising an
**[ITSM request]({{< param dcs_docs_base_url >}}/support/itsm-requests)** to the storage team,
who provision it and return credentials. So if an app needs object storage, plan for a
request, not a `oc apply`.

{{< note >}}
Same {{< param product_short >}} pattern as elsewhere: self-service where it's safe (PVCs
within quota), governed requests for the rest (S3, quota increases).
{{< /note >}}
