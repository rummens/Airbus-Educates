---
title: Summary
---

You took a credential that was leaking in plain sight, moved it into a Kubernetes **Secret**,
wired the workload to reference it, and proved the leak was closed — and you saw, hands-on,
why base64 was never what kept it safe.

## What You Did

- Named the three secret-leak paths: **baked into the image**, **printed to logs**, and
  **inline in a manifest / env dump**.
- Deployed a leaky workload and confirmed the token was exposed in `oc set env --list`.
- Created a **Secret** (`stringData`) and consumed it from a Deployment via `secretKeyRef` —
  a reference, not a literal.
- Verified the fixed deployment's env shows only a **reference**, and base64-**decoded** the
  Secret to prove the encoding is trivially reversible.
- Learned that **RBAC** + **etcd encryption at rest** protect a Secret, and that **sealed /
  external secrets** keep the value out of git entirely.

## Challenge

Do it yourself, unguided: **prove `fixed-app` no longer carries the literal token.** Read its
env with `oc set env deploy/fixed-app --list`, confirm you see a reference to `app-secrets`
and not the plaintext value, then run the check.

```examiner:execute-test
name: verify-no-literal
title: Challenge — the fixed deployment leaks no literal
args:
- fixed-app
- s3cr3t-plaintext-token
- app-secrets
timeout: 15
```

{{< note >}}
**Hint:** `oc set env deploy/fixed-app --list | grep API_TOKEN` — you should see a
`# API_TOKEN from secret app-secrets, key api-token` line, not the token itself.
{{< /note >}}

## Check Your Understanding

1. What are the three common ways a plaintext credential leaks?

{{< note >}}
**Answer:** Baked into the **image** (a `Dockerfile ENV`/`ARG` or copied config), printed to
**logs** (startup config or an error dumping the environment), and inline in a **manifest /
env dump** (a literal `env` value that `get deploy` or `oc set env --list` exposes, and that
lands in git if committed).
{{< /note >}}

2. A Secret's values are base64-encoded. Does that encrypt them — and if not, what actually
   protects a Secret?

{{< note >}}
**Answer:** No. base64 is a reversible **encoding** — `base64 -d` returns the plaintext with
no key. A Secret is protected by **RBAC** (reading it needs the privileged `secrets` verb,
granted narrowly) and by platform **etcd encryption at rest**, not by the encoding.
{{< /note >}}

3. Why is `secretKeyRef` better than putting the value inline as an `env` literal?

{{< note >}}
**Answer:** The literal is readable by anyone with `get deploy` and lands in git if the
manifest is committed. `secretKeyRef` keeps the value in one place — the Secret — so the
workload manifest carries only a reference; reading the actual value then requires separate,
tighter secret-read permission.
{{< /note >}}

## Next Steps

You've handled secrets at the tenant level. The rest of the **Security & Compliance** track
builds on it — image scanning and gates, pod security, supply-chain trust, and the
{{< param product_short >}} governance and EU data-residency obligations that sit behind all
of it.
