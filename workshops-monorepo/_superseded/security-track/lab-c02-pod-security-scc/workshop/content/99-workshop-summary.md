---
title: Summary
---

You saw {{< param product_short >}}'s restricted security policy from both sides — a Pod that
complies sailing through, and a Pod that demands root getting stopped at the door — and you fixed
the second one yourself.

## What You Did

- Learned that **SCC** (OpenShift) and the **Pod Security Standards** (Kubernetes) both gate every
  Pod at admission, and that {{< param product_short >}} namespaces enforce **restricted** /
  **restricted-v2**.
- Understood the **arbitrary-UID** requirement — why an image must not assume a fixed UID or root.
- Deployed a **compliant** Pod and confirmed the `openshift.io/scc` annotation read `restricted-v2`.
- Watched a **root/privileged** Pod get **rejected at admission**, and read the rejection to find
  the violated controls.
- **Remediated** the Pod's `securityContext` (`runAsNonRoot`, `allowPrivilegeEscalation: false`,
  `capabilities.drop: [ALL]`, `seccompProfile: RuntimeDefault`; no `privileged`, no `runAsUser`) and
  watched it be admitted.
- Learned that going above the floor is a governed **Security Exception**, not a self-service toggle.

## Check Your Understanding

1. What are **SCC** and the **Pod Security Standards**, and how do they relate on {{< param product_short >}}?

{{< note >}}
**Answer:** SCC is OpenShift's admission control over what a Pod may do (UIDs, privilege,
capabilities); the Pod Security Standards are the upstream Kubernetes levels (privileged / baseline
/ restricted) enforced per namespace. On {{< param product_short >}} both gate every Pod at
admission — namespaces enforce the **restricted** PSA level and admit Pods under the
**restricted-v2** SCC.
{{< /note >}}

2. Why must an image not assume a fixed UID — least of all root?

{{< note >}}
**Answer:** Restricted-v2 **assigns** an arbitrary, large UID per namespace rather than letting the
Pod choose, and root (UID 0) is forbidden by `runAsNonRoot`. An image that hardcodes a UID or root
will be rejected or fail at runtime. Build for the arbitrary UID: group-0 ownership,
group-writable paths, no privileged ports.
{{< /note >}}

3. Which `securityContext` fields make a Pod restricted-compliant?

{{< note >}}
**Answer:** `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`, and
`seccompProfile.type: RuntimeDefault` — and it must **not** set `privileged: true` or run as
`runAsUser: 0`.
{{< /note >}}

## Challenge

Do it yourself, unguided: **prove your remediated Pod is running under the restricted profile.**
Read the `openshift.io/scc` annotation on `hello-root` and confirm it is `restricted-v2`. Run the
check when ready.

```examiner:execute-test
name: verify-scc-annotation
title: Challenge — hello-root is admitted under restricted-v2
args:
- hello-root
- restricted-v2
timeout: 10
retries: 3
delay: 2
```

{{< note >}}
**Hint:** `oc get pod hello-root -o jsonpath='{.metadata.annotations.openshift\.io/scc}{"\n"}'` —
the same annotation you read for the compliant Pod on page 02. If the Pod isn't there, re-apply
your remediated `pod-root.yaml` first.
{{< /note >}}

## Next Steps

The Security & Compliance track continues with **secrets management** and **supply-chain trust** —
and the **governance** thread (responsibility split, data classification, the exception process)
returns in depth later in the track.
