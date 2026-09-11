---
title: A Name for Something Elsewhere
---

The two types so far both pointed at **your** Pods. An **ExternalName** Service points at
something else entirely.

It has no selector, no endpoints and no proxy. It is a **CNAME** in cluster DNS — an alias.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/externalname
```

## Apply the alias

```editor:open-file
file: ~/exercises/service-externalname.yaml
```

Two fields carry it: `type: ExternalName`, and `externalName` — the host it aliases.

```terminal:execute
command: oc apply -f service-externalname.yaml
```

```examiner:execute-test
name: verify-externalname-created
title: Verify the ExternalName Service aliases the expected host
timeout: 15
retries: .INF
delay: 2
```

Look at it next to the others:

```terminal:execute
command: oc get svc -o wide
```

`api-alias` has **no** cluster IP, **no** ports and an `EXTERNAL-NAME` value. There is nothing
to have endpoints for.

## Resolve it

```terminal:execute
command: getent hosts api-alias.$(oc project -q).svc.cluster.local
```

The answer comes back as the **target's** address, with the target's own name in the output:

```
10.217.4.1    kubernetes.default.svc.cluster.local  api-alias.<your-namespace>.svc.cluster.local
```

That is the CNAME being followed: your name resolved to their name, which resolved to an
address.

```examiner:execute-test
name: verify-externalname-resolves
title: Verify the alias resolves through to its target
timeout: 20
retries: .INF
delay: 2
```

## What it is good for

- **One name your code keeps**, while the thing behind it moves. No redeploy when the address
  changes — edit the Service.
- **Per-environment targets.** The same manifest, a different `externalName` in DEV and PROD.

{{< warning >}}
**⚠️ Watch out:** an alias is not access. {{< param product_short >}} is air-gapped and egress
is **deny-by-default** — a name that resolves does not mean the destination is reachable. An
external destination has to be allowed through the **managed egress proxy** first, which is a
request, not a manifest.
{{< /warning >}}

Next: the two types that look like the obvious way out, and are not.
