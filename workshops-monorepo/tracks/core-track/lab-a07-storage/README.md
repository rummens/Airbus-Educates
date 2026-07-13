# Storage on DCS

**Give a workload data that outlives its container — and prove it survives a restart.**

A container's filesystem is ephemeral: when a Pod restarts, anything written inside is gone.
Most real applications need data to survive — uploads, a database's files, a cache. In this
lab you request persistent storage with a PersistentVolumeClaim, learn how DCS turns that
request into a real disk, mount it into the `hello-dcs` app, and prove the data is still
there after a pod restart. For each concept you'll learn *what* it is, *why* it exists, and
*how* the pieces fit.

- **Track:** Core — DCS Foundations · Lab 7 of 9
- **Audience:** Beginner — comfortable creating a Deployment and running `oc` against your project
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-a02-kubernetes-essentials

## By the end of this lab you'll be able to

- Explain the PVC → StorageClass → PV model and how DCS provisions storage dynamically.
- Distinguish File storage (RWX, shared) from Block storage (RWO, single-writer), and choose the right one.
- Request a volume with a PersistentVolumeClaim and mount it into a workload.
- Prove that data survives a pod restart.
- Explain how data classification drives storage-class choice on DCS, and how object (S3) storage is obtained.

## What you'll do

You'll compare File and Block storage and pick the right class, request a volume with a PVC
and mount it into the sample app, write some data, restart the pod, and confirm the data is
still there. Along the way you'll see how data classification steers storage-class choice
and how S3 object storage is obtained via an ITSM request.
