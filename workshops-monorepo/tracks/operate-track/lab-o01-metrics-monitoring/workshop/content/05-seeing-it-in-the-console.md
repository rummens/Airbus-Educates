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
  ServiceMonitor created. This is where you confirm a scrape is *actually happening*.
- **Developer perspective → Observe** — per-workload CPU, memory and, when your app exposes
  them, its **custom** metrics, without writing any PromQL.

{{< note >}}
**📌 Why this page has no clickable action.** The OpenShift web console cannot be embedded in a
workshop session — it refuses to be framed, and it would be signed in as the session's
identity rather than yours. The console labs in the Console track open it in its own tab
instead, which is how a console tour has to work.
{{< /note >}}

## What to do with a graph

The temptation is to build many. A dashboard that nobody reads during an incident is
decoration.

Three questions are worth a panel each, and they are the ones you can answer with what this lab
already gave you:

- **Is it serving?** Request rate, by Pod. Zero where you expected traffic is the fastest
  signal there is.
- **Is it failing?** The same counter, split by an error label.
- **Is it struggling?** Latency, or CPU against the request you set in **Health & Resources**.

## Where alerts come in

An alert is a PromQL query with a threshold and a duration: *this expression has been true for
five minutes, tell somebody*. You write them as `PrometheusRule` objects, in your own
namespace, exactly like the ServiceMonitor you created here.

That is the next thing this track will cover, and it needs nothing new — only the query
language you have already used.
