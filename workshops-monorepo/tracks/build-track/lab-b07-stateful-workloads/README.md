# Stateful Workloads

**A Deployment's replicas are interchangeable. Some workloads are not.**

A database replica, a queue broker, a cache with its own data on disk — each needs the same
name and the same volume back after a restart. That is a **StatefulSet**.

You create the headless Service it needs, apply a StatefulSet with a **PersistentVolumeClaim
per replica**, and watch replica 0 become ready before replica 1 is even created.

Then you prove the guarantees: address one specific replica by its own DNS name, write
different data into each replica's disk, delete a Pod, and watch the same identity **and** the
same data come back.

Last, scaling — where the asymmetry lives. Scale up and a new disk is provisioned; scale down
and the disk is deliberately **kept**.

> **⚠️ Watch out:** scaling down does not delete volumes. That is a feature, and it is also how
> a storage quota fills up quietly.

- **Track:** Build & Run
- **Audience:** Intermediate
- **Duration:** ~25 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
- **Prerequisites:** Core **Store Data** (you have mounted a PVC once) and **Services & Cluster Networking** (a StatefulSet needs a headless Service).

## By the end of this lab you'll be able to

- Say when a workload needs a StatefulSet rather than a Deployment.
- Explain its three guarantees: stable identity, stable storage, ordered lifecycle.
- Use `volumeClaimTemplates` to give every replica its own claim.
- Address one specific replica by its per-Pod DNS name.
- Predict what a Pod deletion, a scale-up and a scale-down each leave behind.

## What you'll do

1. **Create** the headless Service.
2. **Apply** a 2-replica StatefulSet with a volume per replica.
3. **Resolve** a single replica's own DNS name.
4. **Write** different data into each replica's disk.
5. **Delete** a Pod and check both its identity and its data.
6. **Scale** up and down, and find what was left behind in the quota.
