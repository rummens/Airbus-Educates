---
title: The Same Data, With a Graph
---

Everything you just queried by hand is also in the OpenShift web console, drawn rather than
printed.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/console
```

## Where to look

In the console, signed in as yourself:

- **Observe → Metrics** — a PromQL box and a graph. The same queries you just ran, with a time
  range and a picture.
- **Observe → Targets** — what monitoring is currently scraping, including the target your
  ServiceMonitor created. This is where you confirm that a scrape is happening.
- **Developer perspective → Observe** — per-workload CPU, memory and, when your app exposes
  them, its **custom** metrics, without writing any PromQL.

{{< note >}}
**📌 See it live:** the **Metrics in the console** console lab opens the OpenShift web console
in its own tab and walks you through **Observe** step by step — the same data this page
describes, but on the real page. Run it from the catalog once you have finished this one.
{{< /note >}}

## What to do with a graph

Keep dashboards few. One that nobody reads during an incident is not worth maintaining.

Three questions are worth a panel each, and you can answer them with what you built in this
lab:

- **Is it serving?** Request rate, by Pod. Zero where you expected traffic is the fastest
  signal there is.
- **Is it failing?** The same counter, split by an error label.
- **Is it struggling?** Latency, or CPU against the request you set in **Health & Resources**.

## Where alerts come in

An alert is a PromQL query with a threshold and a duration: *this expression has been true for
five minutes, tell somebody*. You write them as `PrometheusRule` objects, in your own
namespace, exactly like the ServiceMonitor you created here.

Alerts need no new query language, only the PromQL you have already used.
