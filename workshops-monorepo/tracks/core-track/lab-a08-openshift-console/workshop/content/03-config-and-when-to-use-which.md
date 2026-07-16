---
title: Config & When to Use Which
---

The last section, then the judgement call.

## Config ↔ `oc`

The console's **ConfigMaps** and **Secrets** views hold the configuration from A03 —
Secrets shown **masked** in the UI (you reveal a value deliberately, never by accident).
_(screenshot: OpenShift console ConfigMap detail + a masked Secret.)_

```terminal:execute
command: oc get configmap,secret
```

```examiner:execute-test
name: verify-config
title: Verify the Config CLI view runs
timeout: 10
```

## Console or CLI?

Neither is "better" — they're for different moments:

| Reach for the **console** when… | Reach for the **CLI** when… |
|---|---|
| You want a visual overview / Topology | You're scripting or automating |
| A quick one-off inspection or log peek | You need repeatability |
| Onboarding / showing someone around | Doing bulk or fast air-gapped ops |
| Clicking through relationships | Anything you'll do more than once |

## Quick check

You need to do the *same* deployment change across five namespaces, reliably, as part of a
pipeline. Console or CLI?

{{< note >}}
**Answer:** **CLI** — it's scriptable and repeatable. The console is great for looking and
one-offs; automation and bulk/repeatable work belong to `oc`.
{{< /note >}}
