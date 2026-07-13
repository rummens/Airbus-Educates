---
title: Verify There's No Leakage
---

You moved the token into a Secret and wired the workload to reference it. Now prove the leak
is closed — and, at the same time, prove *why* base64 was never the thing protecting it.

## The env dump now shows a reference, not the token

Run the same command you ran against the leaky deployment on page 2 — this time against
`fixed-app`:

```terminal:execute
command: oc set env deploy/fixed-app --list | grep API_TOKEN
```

Compare the output with page 2. There, you saw the literal `s3cr3t-plaintext-token`. Here you
see a **reference** to the Secret — something like:

```
# API_TOKEN from secret app-secrets, key api-token
```

The literal is gone from the workload. Someone with `get deploy` learns only *that* the token
comes from `app-secrets` — not what it is. To read the actual value they now need permission
on the **Secret** itself.

```examiner:execute-test
name: verify-no-literal
title: The env sources the token by reference, not as a literal
args:
- fixed-app
- s3cr3t-plaintext-token
- app-secrets
timeout: 15
```

## The "aha": decode the Secret

So the token now lives in the Secret. Is it *encrypted* there? Read the stored value and
decode it — this needs secret-read RBAC, which is exactly the point:

```terminal:execute
command: oc get secret app-secrets -o jsonpath='{.data.api-token}' | base64 -d; echo
```

The original token prints straight back out:

```
s3cr3t-plaintext-token
```

```examiner:execute-test
name: verify-secret-decodable
title: base64-decoding the Secret returns the token (encoding, not encryption)
args:
- app-secrets
- api-token
- s3cr3t-plaintext-token
timeout: 15
```

That is the whole lesson in one command. base64 is trivially reversible — the encoding hid
nothing. What kept the value safe is that reading it required the `secrets` **RBAC verb** (a
privileged grant), and that the platform encrypts it in **etcd at rest**. The protection is
access control plus at-rest encryption, never the encoding. This is why `get secret` is a
verb you grant sparingly.

## Stronger options DCS offers

A Secret keeps the value out of the workload manifest — but the value is still plaintext in
whatever created the Secret. If that Secret manifest is committed to git, you're back to a
leak. Two patterns close that gap, both platform-supported concepts on {{< param product_short >}}:

- **Sealed Secrets** — commit an *encrypted* SealedSecret to git; only an in-cluster
  controller can decrypt it into a real Secret. Safe to store in a repo.
- **External secret store** — the credential lives in a dedicated secrets manager (a vault),
  and an operator syncs it into the namespace as a Secret. The source of truth never sits in
  git or a manifest at all.

{{< note >}}
Sealed / external secrets are configured platform-side and are out of scope for hands-on here
— see [governance & compliance]({{< param dcs_docs_base_url >}}/governance/overview). For this
lab, the takeaway is the pattern: **the credential belongs in exactly one protected place, and
everything else references it.**
{{< /note >}}

## Cleanup

Your session namespace is torn down automatically when the workshop ends — nothing to remove
by hand. If you want a clean slate to experiment, you can delete what you created:

```terminal:execute
command: oc delete deploy/leaky-app deploy/fixed-app secret/app-secrets --ignore-not-found
```
