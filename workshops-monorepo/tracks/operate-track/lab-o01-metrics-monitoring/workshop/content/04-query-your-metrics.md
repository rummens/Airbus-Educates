---
title: Query Your Own Metrics
---

The samples are being collected. Now ask for them back.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/query
```

## The tenant query endpoint

The platform exposes a query API scoped **per namespace**. Your session's token is all you
need for your own:

```terminal:execute
command: |-
  TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
  NS=$(oc project -q)
  curl -sk -H "Authorization: Bearer $TOKEN" \
    --get "$THANOS_URL/api/v1/query" \
    --data-urlencode "namespace=$NS" \
    --data-urlencode 'query=hello_dcs_up' | head -c 400
  echo
```

```examiner:execute-test
name: verify-metric-queryable
title: Verify your app's metric can be queried back
timeout: 180
retries: .INF
delay: 10
```

{{< note >}}
**⏳ This takes a moment:** the first scrape happens within an interval or two of creating the
ServiceMonitor, so an empty `result` right after is normal. The check waits.
{{< /note >}}

You get JSON: a `result` array, one entry per **series**, each with its `metric` labels and a
`value`. Note the labels the platform added — `namespace`, `pod`, `service` — on top of the
ones your app set.

## Ask a real question

A counter's value is not interesting; its **rate** is. How many requests per second has each
Pod served over the last five minutes?

```terminal:execute
command: |-
  TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
  NS=$(oc project -q)
  curl -sk -H "Authorization: Bearer $TOKEN" \
    --get "$THANOS_URL/api/v1/query" \
    --data-urlencode "namespace=$NS" \
    --data-urlencode 'query=sum by (pod) (rate(hello_dcs_requests_total[5m]))' | head -c 400
  echo
```

```examiner:execute-test
name: verify-promql-rate
title: Verify the PromQL rate query returns a result
timeout: 120
retries: .INF
delay: 10
```

Read the query from the inside out:

1. **`hello_dcs_requests_total[5m]`** — every sample of that metric in the last five minutes.
2. **`rate(...)`** — the per-second increase across that window.
3. **`sum by (pod) (...)`** — collapse the label combinations, keeping one number per Pod.

That is the shape of nearly every dashboard panel you will ever read.

## Now ask about somebody else

Same token, same endpoint, different namespace:

```terminal:execute
command: |-
  TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
  curl -sk -o /dev/null -w 'HTTP %{http_code}\n' -H "Authorization: Bearer $TOKEN" \
    --get "$THANOS_URL/api/v1/query" \
    --data-urlencode "namespace=openshift-monitoring" \
    --data-urlencode 'query=up'
```

```examiner:execute-test
name: verify-cross-namespace-refused
title: Verify a query about another namespace is refused
timeout: 60
retries: .INF
delay: 5
```

**Forbidden.** The endpoint authorizes every query against the namespace you named, using the
same permissions that decide whether you may read Pods there.

That is worth sitting with: **tenancy is enforced in the metrics path too**, not only in the
API. Your metrics are yours, and so is the boundary around them.
