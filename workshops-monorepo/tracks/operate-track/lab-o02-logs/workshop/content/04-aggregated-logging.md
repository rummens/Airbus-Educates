---
title: When the Pod Is Gone
---

`oc logs` reads a file on a node. You often investigate an incident after its Pod or node is
gone, so the platform keeps a copy of every line centrally.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/aggregation
```

## What the platform runs

On **{{< param product_name >}}** a **collector** runs on every node. It reads the same
files `oc logs` reads and ships each line, with labels attached, to a central **log store**,
which on OpenShift is a **LokiStack**.

A central store changes three things:

- **Logs outlive their Pod.** Last night's crash is still there this morning.
- **You can search across workloads**, instead of one Pod at a time.
- **Retention is set by a policy**, not by when the node rotates its files. Somebody decides
  how long lines are kept, and storage is sized for it.

{{< warning >}}
**⚠️ Watch out:** this Academy session has no log store attached, so the queries below are
not runnable here. They are written the way you would run them on a cluster that has one. The
`oc logs` half of this lab is the part you ran yourself.
{{< /warning >}}

## What a query looks like

The query language is **LogQL**, and its shape follows the metrics lab: pick series by
**labels** first, then filter the lines.

```
{namespace="my-team-dev", app="hello-dcs"}
```

That selects every line from that app in that namespace. To narrow it:

```
{namespace="my-team-dev", app="hello-dcs"} |= "FATAL"
```

- **`{...}`** is the label selector. It is cheap, and it always comes first.
- **`|=`** keeps lines containing this string. `!=` excludes, and `|~` is a regular
  expression.

And you can count what you find, which turns logs into a metric:

```
sum by (pod) (rate({namespace="my-team-dev", app="hello-dcs"} |= "FATAL" [5m]))
```

That is the same `rate(...)` and `sum by (...)` from the **Metrics & Monitoring** lab, applied
to log lines instead of samples.

## The same boundary as metrics

A log query is authorized per namespace, exactly like a metric query: you can read your own
tenant's logs and not another's. This matters because secrets often leak through logs.

{{< warning >}}
**⚠️ Never log a secret.** That includes tokens, passwords and request bodies that contain
them. Anything your app prints is copied to a central store, kept for the retention period,
and readable by everyone entitled to your namespace's logs.
{{< /warning >}}

## Making logs worth aggregating

Two habits decide whether the store is searchable:

- **Log in a structured format**, JSON with consistent field names. The collector can parse
  it, and `level="error"` becomes a label rather than a substring.
- **Say what happened once, with identifiers.** One line with a request id, a user id and an
  outcome is worth more than five lines of prose that cannot be correlated.

Where to read them: **Observe → Logs** in the OpenShift console, next to the metrics views from
the previous lab, and the same place an alert links you to.
