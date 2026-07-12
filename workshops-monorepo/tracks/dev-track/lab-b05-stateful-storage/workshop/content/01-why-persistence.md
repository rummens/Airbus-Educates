---
title: Why Persistence?
---

Before adding storage, let's *feel* the problem it solves. Your `hello-dcs` app is running
right now — let's write something inside its container and see what happens on a restart.

## A container's filesystem is ephemeral

Write a file into the running container's own filesystem (not a volume — the container itself):

```terminal:execute
command: oc exec deployment/hello-dcs -- sh -c 'echo "written-inside-the-container" > /tmp/note; cat /tmp/note'
```

You should see the line echoed back:

```
written-inside-the-container
```

It's there — for now. Now replace the pod, exactly as a node drain, a rollout, or a crash
would:

```terminal:execute
command: oc delete pod -l app=hello-dcs
```

The Deployment immediately starts a fresh pod. Give it a moment, then look for your file
in the new container:

```terminal:execute
command: oc exec deployment/hello-dcs -- cat /tmp/note
```

You'll see:

```
cat: /tmp/note: No such file or directory
```

Gone. The new pod is a brand-new container with a **brand-new, empty filesystem**. Nothing
you wrote inside the old container survived. That's not a bug — it's the design: containers
are meant to be disposable and identical.

## Where does data live, then?

Two things you might reach for, and why only one solves this:

- **`emptyDir`** — a scratch volume tied to the *pod*. It survives a container **restart in
  place**, but it's deleted when the pod is removed. Handy for caches and scratch space,
  useless for data you can't lose.
- **A PersistentVolume, requested via a
  [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)** —
  a real disk provisioned by the platform, with a lifecycle **independent of any pod**. Delete
  the pod, the volume stays; a new pod mounts the same volume and the data is right where you
  left it.

That independent lifecycle is the whole point, and it's what you'll build next: request a
volume, mount it into `hello-dcs`, and repeat this exact experiment — but this time the data
will still be there.

{{< note >}}
On {{< param product_short >}} you never pre-create disks. You *claim* storage with a PVC and
the platform's StorageClass provisions a matching volume dynamically — the model you met in
A07. Here you wire that claim into your app.
{{< /note >}}
