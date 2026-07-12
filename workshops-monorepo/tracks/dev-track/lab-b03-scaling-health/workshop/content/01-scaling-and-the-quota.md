---
title: Scaling & the Quota
---

Scaling is how you run more copies of your app — for availability (survive a lost Pod) or
throughput (share the load). You already met [`oc scale`](https://docs.openshift.com/container-platform/latest/applications/deployments/managing-deployment-processes.html)
in Foundations; here the interesting part is the **ceiling**.

## Scale up

Your app runs one replica. Ask for three:

```terminal:execute
command: oc scale deployment/hello-dcs --replicas=3
```

Watch them arrive:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Expected: three `hello-dcs-…` Pods, all `Running` / `1/1`. Confirm:

```examiner:execute-test
name: verify-replicas
title: Deployment scaled to 3 ready replicas
args:
- hello-dcs
- "3"
timeout: 5
retries: 6
delay: 3
```

## Your namespace has a budget

On {{< param product_name >}} your DEV namespace isn't unlimited — it has a
[ResourceQuota](https://docs.openshift.com/container-platform/latest/applications/quotas/quotas-setting-per-project.html)
that caps how much CPU and memory everything in the namespace may **request** in total. Look
at it:

```terminal:execute
command: oc get resourcequota
```

```terminal:execute
command: oc describe quota
```

Expected: a quota showing `requests.cpu` / `requests.memory` **used vs hard** limits. Every
Pod you schedule counts against `used`; when `used` would exceed `hard`, the next Pod is
rejected. Confirm the quota is there:

```examiner:execute-test
name: verify-quota
title: The namespace has a resource quota
timeout: 5
```

{{< note >}}
Think of the namespace as a **resource pool with a cap** — like a resource pool on a VM
cluster. Three small replicas fit easily. The next page asks for far more, on purpose, to see
what the cap does. This budget is a {{< param product_short >}} tenancy control — details at
[{{< param dcs_docs_base_url >}}/namespaces/quotas]({{< param dcs_docs_base_url >}}/namespaces/quotas).
{{< /note >}}
