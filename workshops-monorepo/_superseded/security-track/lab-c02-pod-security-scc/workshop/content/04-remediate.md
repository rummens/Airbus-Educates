---
title: Remediate the Pod
---

You have a rejection message and a checklist. Now fix `pod-root.yaml` so it satisfies every
restricted control, and watch the same Pod get admitted.

## Fix the securityContext

The rejected Pod's `securityContext` asks for root and privilege. You'll replace that whole block
with the compliant one — dropping `privileged` and `runAsUser: 0`, and adding the four controls
restricted requires.

Make sure the file is open so you can watch the change land:

```editor:open-file
file: ~/exercises/pod-root.yaml
```

Now apply the fix:

```editor:replace-matching-text
file: ~/exercises/pod-root.yaml
match: |2
      securityContext:
        runAsUser: 0
        privileged: true
replacement: |2
      securityContext:
        runAsNonRoot: true
        allowPrivilegeEscalation: false
        seccompProfile:
          type: RuntimeDefault
        capabilities:
          drop:
          - ALL
```

Look at what changed, control by control against the rejection:

- `privileged: true` → **removed** (no privileged container).
- `runAsUser: 0` → **removed**, replaced by `runAsNonRoot: true` (let the platform assign an arbitrary UID).
- **added** `allowPrivilegeEscalation: false`.
- **added** `seccompProfile.type: RuntimeDefault`.
- **added** `capabilities.drop: [ALL]`.

The `securityContext` is now identical to the compliant Pod's from page 02 — because "compliant"
is not a mystery, it's just these five things.

## Apply the remediated Pod

```terminal:execute
command: |-
  envsubst < pod-root.yaml | oc apply -f -
```

This time admission accepts it:

```
pod/hello-root created
```

Watch it reach Running:

```terminal:execute
command: oc get pod hello-root -w --request-timeout=60s
```

```examiner:execute-test
name: verify-remediated-running
title: The remediated Pod is admitted and Running
args:
- hello-root
timeout: 120
retries: .INF
delay: 3
```

Same image, same cluster, same restricted namespace — the *only* thing that changed was the
`securityContext`. That's the entire remediation loop: read the rejection, fix the named controls,
re-apply.

## When restricted genuinely isn't enough

Sometimes a workload legitimately needs more than restricted allows — say it must hold a specific
Linux capability, or run at a fixed UID for a legacy reason. On {{< param product_short >}} you
**cannot** simply relax your namespace's policy: the secure floor belongs to the platform, not the
tenant.

Instead, needing **baseline** (or any capability above the floor) is handled as a **Security
Exception** — a governed request, raised through the process, reviewed and granted for that specific
workload. It is deliberate and auditable, never a self-service toggle. The first move is always to
fix the image so it doesn't need the exception; the exception is the last resort, not the default.

{{< note >}}
The Security Exception process, the platform/tenant responsibility split, and data classification
are {{< param product_short >}} **governance** concepts. See the
[{{< param product_short >}} governance overview]({{< param dcs_docs_base_url >}}/governance/overview).
The governance thread is picked up in depth later in the Security & Compliance track.
{{< /note >}}
