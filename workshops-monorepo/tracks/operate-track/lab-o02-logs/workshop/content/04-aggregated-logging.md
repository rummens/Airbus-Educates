---
title: When the Pod Is Gone
---

`oc logs` reads a file on a node. Aggregation exists because incidents outlive nodes.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/aggregation
```

## What the platform runs

On **{{< param product_name >}}** a **collector** runs on every node. It reads the same files
`oc logs` reads and ships each line, with labels attached, to a central **log store** — a
**LokiStack** on OpenShift.

Three things change the moment that exists:

- **Logs outlive their Pod.** Last night's crash is still there this morning.
- **You can search across workloads**, instead of one Pod at a time.
- **Retention is a policy**, not an accident of file rotation — somebody decides how long, and
  storage is paid for accordingly.

{{< warning >}}
**⚠️ Watch out:** this Academy session has no log store attached, so the queries below are not
runnable here — they are written the way you will run them on a cluster that has one. The
`oc logs` half of this lab is the part you just practised for real.
{{< /warning >}}

## What a query looks like

The query language is **LogQL**, and its shape will look familiar after the metrics lab: pick
series by **labels** first, then filter the lines.

```
{namespace="my-team-dev", app="hello-dcs"}
```

Everything from that app in that namespace. Then narrow it:

```
{namespace="my-team-dev", app="hello-dcs"} |= "FATAL"
```

- **`{...}`** — the label selector. Cheap, and always first.
- **`|=`** — keep lines containing this string. (`!=` excludes, `|~` is a regular expression.)

And you can count what you find, which turns logs into a metric:

```
sum by (pod) (rate({namespace="my-team-dev", app="hello-dcs"} |= "FATAL" [5m]))
```

That is the same `rate(...)` and `sum by (...)` from the **Metrics & Monitoring** lab, applied
to log lines instead of samples.

## The same boundary as metrics

A log query is authorized per namespace, exactly like a metric query: you can read your own
tenant's logs and not another's.

That is worth saying plainly, because logs are where secrets leak. Which leads to the only
rule on this page you must not skip.

{{< warning >}}
**⚠️ Never log a secret.** Not a token, not a password, not a full request body containing
either. Anything your app prints is copied to a central store, kept for the retention period,
and readable by everyone entitled to your namespace's logs. `oc logs` feels private; the
aggregate is not.
{{< /warning >}}

## Making logs worth aggregating

Two habits make the difference between a store you search and a store you grep in despair:

- **Log in a structured format** — JSON with consistent field names. The collector can parse
  it, and `level="error"` becomes a label rather than a substring.
- **Say what happened, once, with identifiers.** One line with a request id, a user id and an
  outcome beats five lines of prose that cannot be correlated with anything.

Where to read them: **Observe → Logs** in the OpenShift console, next to the metrics views from
the previous lab, and the same place an alert links you to.
