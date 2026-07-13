# Stateful Workloads & Storage

**A pod is ephemeral — give your app storage that outlives it, and prove data survives a restart.**

Anything written inside a container is gone the moment its pod is replaced, and pods get replaced readily. Most real apps need data to survive — uploads, a database's files, a queue. In this lab you take the stateless `hello-dcs` app you already know and give it persistence on the Digital Container Service (DCS): request a PersistentVolumeClaim from a DCS storage class, mount it, write to it, and prove the data outlives a pod restart. This is the developer's view of storage — wiring a volume into your own app.

- **Track / module:** Developer — Build on DCS (Module B) · Lab 5 of 6
- **Audience:** Intermediate — comfortable creating and scaling a Deployment with `oc`
- **Duration:** ~35 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-b01-deploy-first-app · recommended: lab-a07-storage for the platform view · assumes Foundations (lab-a02-kubernetes-essentials)

## By the end of this lab you'll be able to

- Request storage with a PersistentVolumeClaim and choose an appropriate DCS storage class
- Mount a volume into your app and write to it
- Explain access modes (RWO vs RWX) and when each applies
- Prove that data survives a pod restart, and reason about why a single volume doesn't fan out to many replicas

## What you'll do

Starting from the already-running `hello-dcs` app, you confirm a container's filesystem is ephemeral, request a PVC from a DCS storage class (parameterised, never hard-coded), mount it into the app and write data, then delete the pod and watch the data still be there when the replacement comes up. This lab is self-contained and optional in the B chain — skipping it won't block lab-b06.

## Before you start

Finish lab-b01-deploy-first-app first — you should be comfortable creating and scaling a Deployment with `oc`. lab-a07-storage is recommended for the platform-level view of PVCs and DCS storage classes; this lab puts one to work rather than re-explaining it.
