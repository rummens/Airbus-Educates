---
title: Watch a Root Pod Get Rejected
---

Now the failure case. This Pod asks to run as **root** in a **privileged** container — the two
things the restricted policy most firmly forbids. Watch admission stop it dead.

## Read what it's asking for

Open the manifest:

```editor:open-file
file: ~/exercises/pod-root.yaml
```

The `securityContext` is the whole problem:

```editor:select-matching-text
file: ~/exercises/pod-root.yaml
text: |2
      securityContext:
        runAsUser: 0
        privileged: true
```

- `runAsUser: 0` — run as **root**. Violates `runAsNonRoot`.
- `privileged: true` — a privileged container with near-total host access. Forbidden outright.

And by omission it also fails the rest: no `allowPrivilegeEscalation: false`, no
`capabilities.drop: [ALL]`, no `seccompProfile`. Every restricted control is broken.

## Apply it — and expect a rejection

{{< warning >}}
**This command is *meant* to fail.** The error you're about to see is the lesson, not a mistake on
your part. Read it carefully.
{{< /warning >}}

```terminal:execute
command: |-
  envsubst < pod-root.yaml | oc apply -f -
```

Instead of `pod/hello-root created`, you'll see an admission error — the Pod is refused before it is
ever created. The message names the controls it violated, for example:

```
Error from server (Forbidden): error when creating "STDIN": pods "hello-root" is forbidden:
violates PodSecurity "restricted:latest": privileged (container "hello-root" must not set
securityContext.privileged=true), allowPrivilegeEscalation != false, unrestricted capabilities,
runAsNonRoot != true (...), seccompProfile (...)
```

(The exact wording varies with the cluster, and you may also see a Security Context Constraint
denial — both gates reject it.)

## Confirm nothing was created

Because the Pod was rejected at admission, it was never created — there's nothing to run:

```terminal:execute
command: oc get pod hello-root
```

You should see:

```
Error from server (NotFound): pods "hello-root" not found
```

That "not found" is the point: the apply was **denied**, so no `hello-root` Pod exists.

```examiner:execute-test
name: verify-root-rejected
title: The root/privileged Pod was rejected at admission
args:
- hello-root
timeout: 10
retries: 3
delay: 2
```

## Read the rejection

This is a skill worth practising: the rejection tells you exactly what to fix. From the message
above, the violated controls are:

- **`privileged`** — must not be `true`.
- **`runAsNonRoot`** — the container must not run as root (here `runAsUser: 0`).
- **`allowPrivilegeEscalation`** — must be `false`.
- **`unrestricted capabilities`** — must `drop: [ALL]`.
- **`seccompProfile`** — must be set (e.g. `RuntimeDefault`).

That list *is* your remediation checklist. On the next page you'll work through it and turn this Pod
into one admission accepts.
