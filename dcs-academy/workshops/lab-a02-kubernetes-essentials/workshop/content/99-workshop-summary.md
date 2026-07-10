---
title: Summary
---

You deployed a real application on **{{< param product_name >}}** and worked through the
core Kubernetes workload concepts — not just running commands, but seeing *why* each
piece exists and how they fit together.

## What You Did

- Compared **imperative vs declarative** management and previewed changes with `--dry-run`.
- Created a **Deployment** from a manifest and watched it roll out.
- Saw how a Deployment owns a **ReplicaSet**, which owns **Pods**, and why you manage the top of that chain.
- Used **labels and selectors** — the glue that links Deployments, Services, and Pods.
- Inspected resources with `oc get`, `oc describe`, and `oc explain`.
- **Scaled** the app and watched Kubernetes **self-heal** a deleted Pod, and learned about configuration drift.
- Read **logs** and used **`oc exec`** to look inside a container.
- Gave the app a stable address with a **Service** and reached it by in-cluster **DNS**.

## Challenge

Now do it yourself, unguided. **Scale the `hello-dcs` Deployment to 2 replicas**, keeping
within your project quota. When you think it's done, run the check.

```examiner:execute-test
name: verify-replicas
title: Challenge — deployment scaled to 2 replicas
args:
- hello-dcs
- "2"
timeout: 5
retries: 5
delay: 2
```

{{< note >}}
**Hint:** you scaled *up* earlier with `oc scale deployment/<name> --replicas=<n>`. The
same command scales down. (For a lasting change you'd edit the manifest — but for this
quick check, the imperative command is fine.)
{{< /note >}}

{{< note >}}
**Reveal solution** — if you're stuck, run this:

```terminal:execute
command: oc scale deployment/hello-dcs --replicas=2
```
{{< /note >}}

## Check Your Understanding

1. Why is the **declarative** approach (`oc apply` from a file) preferred over imperative commands for anything lasting?

{{< note >}}
**Answer:** The file is the source of truth — you can review it, keep it in git, and
re-apply it anywhere. Imperative changes leave no record and cause configuration drift.
{{< /note >}}

2. A Deployment created a ReplicaSet and Pods. If you delete a **Pod**, what happens, and why?

{{< note >}}
**Answer:** The ReplicaSet immediately creates a replacement to keep the desired replica
count — self-healing. That's why you never manage Pods directly; change the Deployment.
{{< /note >}}

3. What connects a **Service** to the specific Pods it should send traffic to?

{{< note >}}
**Answer:** The label selector. The Service routes to all Pods whose labels match its
`spec.selector` (here `app: hello-dcs`), and this set updates automatically.
{{< /note >}}

4. Why must you use a Service's **DNS name** rather than a Pod's IP address?

{{< note >}}
**Answer:** Pod IPs change whenever a Pod is replaced. The Service provides a stable name
and IP and load-balances across the current Pods.
{{< /note >}}

5. You ran `oc scale` to 3 but your manifest says 1 replica. What is this called, and how do you fix it?

{{< note >}}
**Answer:** Configuration drift. Re-apply the manifest (`oc apply`) to bring the cluster
back in line with your source of truth.
{{< /note >}}

## Next Steps

Next in Foundations: **Namespaces & the Prod/Dev Model**, where you'll meet
{{< param product_short >}}'s DEV and PROD namespaces.
