---
title: Config & When to Use Which
---

The last console section, then how to choose between the console and the CLI.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/config
```

## Config ↔ `oc`

The console's **ConfigMaps** and **Secrets** views hold the configuration from A02 —
Secrets are shown **masked** in the UI, so a value is revealed only when you choose to.
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

Neither is "better" — each fits a different task:

| Reach for the **console** when… | Reach for the **CLI** when… |
|---|---|
| You want a visual overview or Topology | You are scripting or automating |
| A quick one-off inspection or a log check | You need a repeatable result |
| Onboarding or showing someone around | Doing bulk or fast air-gapped operations |
| Exploring how resources relate | Anything you will do more than once |

## Quick check

You need to do the *same* deployment change across five namespaces, reliably, as part of a
pipeline. Console or CLI?

{{< note >}}
**Answer:** **CLI** — it is scriptable and repeatable. The console is best for viewing and
one-off actions; automation and bulk or repeatable work belong to `oc`.
{{< /note >}}
