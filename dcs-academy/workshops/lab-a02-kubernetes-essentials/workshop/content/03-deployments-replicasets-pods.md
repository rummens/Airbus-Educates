---
title: Deployments, ReplicaSets, and Pods
---

You created one Deployment — but it quietly created two other kinds of resource. Ask
Kubernetes for everything labelled `app=hello-dcs`:

```terminal:execute
command: oc get all -o name -l app=hello-dcs
```

You should see something like:

```
pod/hello-dcs-6b8999855c-6jjhj
service/… (later)
deployment.apps/hello-dcs
replicaset.apps/hello-dcs-6b8999855c
```

So one Deployment produced a **ReplicaSet** and a **Pod**. Why three resources?

## A Chain of Templates

- A **[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)** describes your desired state and manages rollouts. It is a template for…
- a **[ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)**, whose one job is to keep the right number of Pods running. It is a template for…
- **[Pods](https://kubernetes.io/docs/concepts/workloads/pods/)** — the actual running instances of your application (one or more containers).

Each layer owns the one below. When you change the image or replica count on the
Deployment, it creates a new ReplicaSet or adjusts the existing one, which in turn
creates or removes Pods.

Confirm the Pod is running:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Expected (status `Running`, `1/1` ready):

```
NAME                         READY   STATUS    RESTARTS   AGE
hello-dcs-6b8999855c-6jjhj   1/1     Running   0          1m
```

```examiner:execute-test
name: verify-pods-running
title: Verify the pod is running
args:
- hello-dcs
- "1"
timeout: 10
```

## Manage the Top, Not the Bottom

Because of this ownership chain, two rules follow:

- **Always change the Deployment**, never the ReplicaSet or Pod directly. If you edit a
  Pod, the ReplicaSet will happily replace it and your change vanishes. Change flows
  *down* from the Deployment.
- **Deleting the Deployment deletes everything under it** — the ReplicaSet and Pods are
  owned by it and are cleaned up automatically. You don't delete them one by one.

```examiner:execute-test
name: verify-deployment-exists
title: Verify the deployment exists
args:
- hello-dcs
timeout: 10
```
