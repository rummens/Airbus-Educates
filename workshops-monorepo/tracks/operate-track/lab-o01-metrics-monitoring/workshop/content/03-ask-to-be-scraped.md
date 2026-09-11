---
title: Ask to Be Scraped
---

You do not configure the platform's Prometheus. You put an object in **your own namespace**
that says what to collect, and the platform finds it.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/servicemonitor
```

## The ServiceMonitor

```editor:open-file
file: ~/exercises/servicemonitor.yaml
```

Three fields carry it, and two of them are where mistakes live:

- **`selector.matchLabels`** — which **Service** to scrape. It matches the *Service's* labels,
  not the Pods'.
- **`endpoints.port`** — the Service's port **by name**. A numeric port here does not work,
  and an unnamed Service port cannot be scraped at all.
- **`interval`** — how often. Every sample costs storage that somebody pays for.

```terminal:execute
command: oc apply -f servicemonitor.yaml
```

```examiner:execute-test
name: verify-servicemonitor-created
title: Verify the ServiceMonitor exists and selects your Service
timeout: 30
retries: .INF
delay: 3
```

{{< note >}}
**📌 Note:** you were able to create that because your namespace is entitled to
`monitoring.coreos.com` objects. Being able to *ask* is itself a permission — the **RBAC &
Tenancy** lab is where that idea came from.
{{< /note >}}

## Confirm it is selecting something

A ServiceMonitor that matches nothing looks exactly like one that works:

```terminal:execute
command: |-
  oc get servicemonitor hello-dcs -o jsonpath='{.spec.selector.matchLabels}{"\n"}'
  oc get svc -l app=hello-dcs
```

```examiner:execute-test
name: verify-selector-matches
title: Verify the selector actually matches a Service with a named port
timeout: 30
retries: .INF
delay: 3
```

If the labels on the left do not appear on a Service on the right, nothing will ever be
scraped — and nothing will tell you so.

{{< warning >}}
**⚠️ Watch out:** a ServiceMonitor never reports an error for selecting nothing. No error, no
data, no clue. Checking the selector by hand, as you just did, is the whole debugging
technique.
{{< /warning >}}

## Wait for the first scrape

Collection starts within about an interval or two. The next page queries the result, and the
check there waits for the series to appear.
