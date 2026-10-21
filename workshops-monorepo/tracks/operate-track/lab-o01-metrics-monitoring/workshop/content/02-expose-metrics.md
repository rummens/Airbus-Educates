---
title: What the App Says
---

Before anything can scrape your app, the app has to expose metrics.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/expose
```

## Read the endpoint

`hello-dcs` serves metrics on `/metrics`. Ask it directly, through the Service:

```terminal:execute
command: curl -s "http://hello-dcs.$(oc project -q).svc:8080/metrics"
```

```examiner:execute-test
name: verify-metrics-endpoint
title: Verify the app serves Prometheus exposition format
timeout: 60
retries: .INF
delay: 3
```

## Read the format

The format is plain text, with three kinds of line.

```
# HELP hello_dcs_requests_total Requests served, by path.
# TYPE hello_dcs_requests_total counter
hello_dcs_requests_total{path="/"} 12
```

- **`# HELP`** says what the metric means, for whoever reads it later.
- **`# TYPE`** says `counter` (only goes up), `gauge` (goes up and down), or one of a couple
  of others.
- **the sample** is the metric **name**, its **labels** in braces, and the value.

Labels are what make one metric useful: `path="/"` and `path="/healthz"` are separate series
of the same metric, and you can sum, filter or split by them later.

{{< note >}}
**💡 Tip:** a **counter** never goes down, so its raw value is rarely interesting. What you
want is how fast it rises, which is `rate(...)`. That is why counters are named `_total` by
convention.
{{< /note >}}

## Generate some traffic

Send 60 requests so the counter has something to count:

```terminal:execute
command: |-
  url="http://hello-dcs.$(oc project -q).svc:8080"
  for i in $(seq 1 60); do curl -s -o /dev/null "$url"; done
  echo "sent 60 requests"
  curl -s "$url/metrics" | grep hello_dcs_requests_total
```

```examiner:execute-test
name: verify-counter-moved
title: Verify the request counter has counted your traffic
timeout: 60
retries: .INF
delay: 3
```

The counter for `path="/"` has moved. The two replicas each count **their own** requests,
and you are looking at whichever one the Service picked.

That is why the next step collects from **all** endpoints rather than from one.
