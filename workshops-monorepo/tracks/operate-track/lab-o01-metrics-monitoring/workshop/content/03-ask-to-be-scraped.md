---
title: Ask to Be Scraped
---

You put an object in **your own namespace** that says what to collect, and the platform's
monitoring picks it up.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/servicemonitor
```

## The ServiceMonitor

```editor:open-file
file: ~/exercises/servicemonitor.yaml
```

Three fields matter, and two of them cause most mistakes:

- **`selector.matchLabels`** picks which **Service** to scrape. It matches the *Service's*
  labels, not the Pods'.
- **`endpoints.port`** names the Service's port **by name**. A numeric port does not work, and
  an unnamed Service port cannot be scraped at all.
- **`interval`** sets how often. Every sample costs storage.

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
`monitoring.coreos.com` objects. Being able to ask is itself a permission, which is the
subject of the **RBAC & Tenancy** lab.
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
scraped, and nothing will tell you so.

{{< warning >}}
**⚠️ Watch out:** a ServiceMonitor never reports an error for selecting nothing; it collects no
data. Checking the selector by hand, as you just did, is how you debug it.
{{< /warning >}}

## Wait for the first scrape

Collection starts within about an interval or two. The next page queries the result, and the
check there waits for the series to appear.
