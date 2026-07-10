---
title: Creating Resources
---

Before you create anything, it's worth understanding the two ways to manage resources on
Kubernetes — because the choice matters more than it first appears.

## Imperative vs Declarative

With the **imperative** style you tell Kubernetes *what to do* with a command, for
example "create a deployment called blog". With the **declarative** style you write down
*the desired state* in a YAML file and tell Kubernetes to make reality match it with
`oc apply`.

Both create the same objects. The difference shows up later:

- Imperative commands are quick to type but leave **no record** of what you did. Reproducing the setup later, or reviewing a change, is hard.
- Declarative files are **the source of truth**. You keep them in git, review changes, and re-apply them to any cluster. This is how you run things in production.

Kubernetes documents both approaches — [imperative commands](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/imperative-command/) and [declarative configuration](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/). We'll use a command to *generate* a starting point, then switch to declarative files for everything real.

## Preview Without Creating: `--dry-run`

`oc create deployment` can build a Deployment for you. Rather than run it for real, ask
it to show what it *would* create with `--dry-run=client -o yaml`:

```terminal:execute
command: |-
  oc create deployment hello-dcs --image=$DCS_REGISTRY/samples/hello-dcs:1.0 --port=8080 --replicas=2 --dry-run=client -o yaml
```

You should see a full Deployment manifest printed to the terminal — something like:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: hello-dcs
  name: hello-dcs
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-dcs
  template:
    metadata:
      labels:
        app: hello-dcs
    spec:
      containers:
      - image: harbor.example.dcs/dcs-academy/samples/hello-dcs:1.0
        name: hello-dcs
        ports:
        - containerPort: 8080
...
```

`--dry-run=client` means *don't create anything — just show me, and validate it*. It's
the safe way to check a command or manifest before it touches the cluster. Nothing was
created, which we can confirm:

```terminal:execute
command: oc get deployment hello-dcs
```

You should see:

```
Error from server (NotFound): deployments.apps "hello-dcs" not found
```

That "not found" is the point — the dry run created nothing.

```examiner:execute-test
name: verify-deployment-absent
title: Verify the dry-run created nothing
args:
- hello-dcs
timeout: 10
```

{{< note >}}
Unsure what a command or field does? `oc <command> --help` explains any command, and
`oc explain <resource>` (e.g. `oc explain deployment.spec`) documents any resource field.
{{< /note >}}
