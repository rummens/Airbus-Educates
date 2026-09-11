---
title: Promotion
---

You now have the same app running in both namespaces. In real work they would not have got
there the same way.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/promotion
```

## Compare what is actually running

```terminal:execute
command: |-
  echo "--- DEV ---"
  oc get deploy hello-dcs -n $DEV_NS -o jsonpath='{.spec.template.spec.containers[0].resources}{"\n"}'
  echo "--- PROD ---"
  oc get deploy hello-dcs -n $PROD_NS -o jsonpath='{.spec.template.spec.containers[0].resources}{"\n"}'
```

```examiner:execute-test
name: verify-both-running
title: Verify the app is running in both namespaces
timeout: 60
retries: .INF
delay: 3
```

DEV took the namespace defaults. PROD carries the numbers you declared. **Two different
running states from two different manifests** — which is exactly the thing promotion is meant
to prevent.

## What promotion is

Promotion is moving a **known, tested artefact** from DEV to PROD, unchanged. Two parts, and
both matter:

1. **The same image.** Not "rebuilt from the same branch" — the *same image*, identified by
   its tag or digest. On {{< param product_short >}} it arrives in the PROD project either
   from the **green catalog** of cleared images, or **mirrored from the DEV project** — a
   request, not a self-service push.
2. **The same manifest**, with only environment-specific values differing (replica count,
   config, hostnames). Sized, because PROD will not admit it otherwise.

## What promotion is not

**Editing PROD in place.**

Two reasons, and the second is the one that hurts:

- a change nobody made in DEV has never been tested anywhere;
- the next promotion **overwrites it**, silently, and the thing that was keeping PROD working
  disappears.

{{< warning >}}
**⚠️ Watch out:** "just this one hotfix directly in PROD" is how environments drift apart. The
fix belongs in DEV, gets tested there, and is promoted — even when that feels slower during an
incident.
{{< /warning >}}

## Where the policy fits

PROD's refusal earlier was not an obstacle to route around. It was the platform checking that
what you are promoting is **promotable**:

- sized, so it can be scheduled and paid for;
- explicit, so the next person can read what it needs;
- and only then publishable, through a Route on the controlled edge.

The same posture is why the registry has a cleared catalog and a CVE threshold for PROD pulls:
by the time something reaches a PROD namespace, several independent things have each said yes.

## Clean up the DEV attempt

```terminal:execute
command: oc delete deploy,svc hello-dcs -n $DEV_NS --ignore-not-found
```

```examiner:execute-test
name: verify-dev-cleaned
title: Verify the DEV namespace was cleaned up
timeout: 60
retries: .INF
delay: 3
```

PROD keeps running — which, after a promotion, is the whole idea.
