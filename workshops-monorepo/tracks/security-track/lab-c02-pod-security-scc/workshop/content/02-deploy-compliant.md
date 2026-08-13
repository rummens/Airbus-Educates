---
title: Deploy a Compliant Pod
---

Start with the happy path: a Pod whose `securityContext` already meets the restricted bar. You'll
apply it, watch it reach Running, and confirm *which* SCC admitted it.

## Read the securityContext

Open the manifest and look at the `securityContext` block:

```editor:open-file
file: ~/exercises/pod-compliant.yaml
```

The four restricted controls from the previous page are all here, on the container:

```editor:select-matching-text
file: ~/exercises/pod-compliant.yaml
text: |2
      securityContext:
        runAsNonRoot: true
        allowPrivilegeEscalation: false
        seccompProfile:
          type: RuntimeDefault
        capabilities:
          drop:
          - ALL
```

- `runAsNonRoot: true` — refuse to run as UID 0.
- `allowPrivilegeEscalation: false` — no climbing to more privileges.
- `seccompProfile.type: RuntimeDefault` — apply the default syscall filter.
- `capabilities.drop: [ALL]` — hold no Linux capabilities.

Notice what's *not* here: no `runAsUser`. We don't pick a UID — the platform assigns an arbitrary
one, and because the image doesn't assume any particular user, that's fine.

## Apply it

Apply the manifest. `envsubst` fills in the registry value first:

```terminal:execute
command: |-
  envsubst < pod-compliant.yaml | oc apply -f -
```

Expected output:

```
pod/hello-compliant created
```

That the apply *succeeded* is already the first result: admission accepted this Pod.

## Watch it start

The node pulls the image from Harbor and starts the container — give it a few seconds. "Done" is
the Pod reaching **Running**:

```terminal:execute
command: oc get pod hello-compliant -w --request-timeout=60s
```

```examiner:execute-test
name: verify-compliant-running
title: The compliant Pod is admitted and Running
args:
- hello-compliant
timeout: 120
retries: .INF
delay: 3
```

## Which SCC admitted it?

When a Pod is admitted, OpenShift records the SCC it was admitted under in an annotation. Read it:

```terminal:execute
command: oc get pod hello-compliant -o jsonpath='{.metadata.annotations.openshift\.io/scc}{"\n"}'
```

You should see:

```
restricted-v2
```

That annotation is the proof of which security profile your Pod is running under. `restricted-v2`
is the locked-down default every compliant tenant workload lands on.

```examiner:execute-test
name: verify-scc-annotation
title: The Pod was admitted under the restricted-v2 SCC
args:
- hello-compliant
- restricted-v2
timeout: 10
retries: 3
delay: 2
```

{{< note >}}
The escaped `openshift\.io/scc` in the JSONPath is intentional — the dot in the annotation key is
part of the name, so it must be escaped rather than read as a path separator.
{{< /note >}}

A well-behaved Pod is admitted, assigned an arbitrary UID, and runs. Next, watch what happens when a
Pod ignores the rules.
