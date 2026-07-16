# Storage

**Give your app memory that outlives its Pod — request a volume, write to it, restart, and watch the data survive.**

Everything your app has written so far vanished the moment a Pod restarted. This lab fixes
that: you request a **PersistentVolumeClaim** from a DCS storage class, mount it into the
app, write a marker, delete the Pod, and read the marker back — proof that the volume
persists independently of the container. Then it covers the choices that matter on DCS:
**File vs Block**, why data classification drives the storage class, and how object (S3)
storage is requested.

- **Track:** Core / Fundamentals · Lab 5
- **Audience:** Intermediate — you've done A02 (A03/A04 helpful)
- **Duration:** ~30 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** A02 (Deploy Your First App).

## By the end of this lab you'll be able to

- Explain the PVC → StorageClass → PV model and dynamic provisioning.
- Request a volume with a PVC and mount it into the app.
- Prove data persists across a Pod restart.
- Distinguish File (RWX) from Block (RWO) storage and when to use each.
- State that classification drives storage-class choice, and that S3 comes via an ITSM ticket.

## What you'll do

Look at the storage classes DCS offers, claim a File volume, mount it, write a marker,
restart the Pod, and confirm the marker is still there — then, as a challenge, claim a
Block volume too.
