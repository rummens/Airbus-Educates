# Storage

**Give your app memory that outlives its Pod — request a volume, write to it, restart, and watch the data survive.**

Everything your app has written so far vanished the moment a Pod restarted.

This lab fixes that. You request a **PersistentVolumeClaim** from a DCS storage class, mount
it into the app, write a marker, delete the Pod, and read the marker back — proof that the
volume persists independently of the container.

Then it covers the choices that matter on DCS:

- **File vs Block** storage;
- why **data classification** drives the storage class;
- how **object (S3)** storage is requested.

- **Track:** Core / Fundamentals
- **Audience:** Beginner — you've done the **Deploy Your First App** lab (**Configure & Troubleshoot Your App** and **Expose Your App** help)
- **Duration:** ~20 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** the **Deploy Your First App** lab.

## By the end of this lab you'll be able to

- Explain the PVC → StorageClass → PV model and dynamic provisioning.
- Request a volume with a PVC and mount it into the app.
- Prove data persists across a Pod restart.
- Distinguish File (RWX) from Block (RWO) storage and when to use each.
- State that classification drives storage-class choice, and that S3 comes via an ITSM ticket.

## What you'll do

1. **Look** at the storage classes DCS offers.
2. **Claim** a File volume and mount it.
3. **Write** a marker, restart the Pod, and confirm the marker is still there.
4. **Challenge:** claim a Block volume too.
