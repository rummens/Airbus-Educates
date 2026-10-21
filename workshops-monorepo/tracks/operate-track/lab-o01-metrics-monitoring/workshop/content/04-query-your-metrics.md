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

```section:begin
name: breakdown-query-up
prefix: Breakdown
title: What each part of the command does
```

- **`TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)`** — reads your session's ServiceAccount token from the file every Pod gets, and stores it in the variable `TOKEN`.
- **`NS=$(oc project -q)`** — stores your namespace name in the variable `NS`; `-q` prints only the name.
- **`curl -sk`** — `-s` hides the progress bar; `-k` skips TLS certificate verification for this in-cluster endpoint.
- **`-H "Authorization: Bearer $TOKEN"`** — sends the token, so the endpoint knows who is asking and checks your permissions.
- **`--get "$THANOS_URL/api/v1/query"`** — calls the query API with a GET request; `$THANOS_URL` is already set in your session and points at the platform's tenant query endpoint. `--get` turns the `--data-urlencode` values below into URL parameters.
- **`--data-urlencode "namespace=$NS"`** — names the namespace you are asking about. The endpoint authorizes the query against this namespace.
- **`--data-urlencode 'query=hello_dcs_up'`** — the PromQL query, URL-encoded so its characters survive the trip.
- **`| head -c 400`** — shows only the first 400 characters of the JSON answer.
- **`echo`** — prints a newline, because the cut-off output does not end with one.

```section:end
name: breakdown-query-up
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

You get JSON: a `result` array, one entry per **series**, each with its `metric` labels and
a `value`. The platform added `namespace`, `pod` and `service` on top of the labels your app
set.

## Ask a real question

A counter's value is rarely interesting; its **rate** is. How many requests per second has
each Pod served over the last five minutes?

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

```section:begin
name: breakdown-query-rate
prefix: Breakdown
title: What each part of the command does
```

- **`TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)`** — reads your session's ServiceAccount token from the file every Pod gets, and stores it in the variable `TOKEN`.
- **`NS=$(oc project -q)`** — stores your namespace name in the variable `NS`; `-q` prints only the name.
- **`curl -sk`** — `-s` hides the progress bar; `-k` skips TLS certificate verification for this in-cluster endpoint.
- **`-H "Authorization: Bearer $TOKEN"`** — sends the token, so the endpoint knows who is asking and checks your permissions.
- **`--get "$THANOS_URL/api/v1/query"`** — calls the query API with a GET request; `$THANOS_URL` is already set in your session and points at the platform's tenant query endpoint. `--get` turns the `--data-urlencode` values below into URL parameters.
- **`--data-urlencode "namespace=$NS"`** — names the namespace you are asking about. The endpoint authorizes the query against this namespace.
- **`--data-urlencode 'query=…'`** — the PromQL query (explained below the command), URL-encoded so its spaces, brackets and parentheses survive the trip.
- **`| head -c 400`** — shows only the first 400 characters of the JSON answer.
- **`echo`** — prints a newline, because the cut-off output does not end with one.

```section:end
name: breakdown-query-rate
```

```examiner:execute-test
name: verify-promql-rate
title: Verify the PromQL rate query returns a result
timeout: 120
retries: .INF
delay: 10
```

Read the query from the inside out:

1. **`hello_dcs_requests_total[5m]`** is every sample of that metric in the last five
   minutes.
2. **`rate(...)`** is the per-second increase across that window.
3. **`sum by (pod) (...)`** collapses the label combinations, keeping one number per Pod.

That is the shape of most dashboard panels you will read.

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

```section:begin
name: breakdown-query-other-namespace
prefix: Breakdown
title: What each part of the command does
```

- **`TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)`** — reads your session's ServiceAccount token from the file every Pod gets, and stores it in the variable `TOKEN`.
- **`curl -sk`** — `-s` hides the progress bar; `-k` skips TLS certificate verification for this in-cluster endpoint.
- **`-o /dev/null`** — throws away the response body.
- **`-w 'HTTP %{http_code}\n'`** — after the request, prints only the HTTP status code.
- **`-H "Authorization: Bearer $TOKEN"`** — sends the token, so the endpoint knows who is asking and checks your permissions.
- **`--get "$THANOS_URL/api/v1/query"`** — the same query API as before, called with a GET request.
- **`--data-urlencode "namespace=openshift-monitoring"`** — a namespace that is not yours. This is what the endpoint refuses.
- **`--data-urlencode 'query=up'`** — a simple query; the namespace decides the answer, not the query.

```section:end
name: breakdown-query-other-namespace
```

```examiner:execute-test
name: verify-cross-namespace-refused
title: Verify a query about another namespace is refused
timeout: 60
retries: .INF
delay: 5
```

You get **Forbidden** (HTTP 403). The endpoint authorizes every query against the namespace you named, using
the same permissions that decide whether you may read Pods there, so metrics queries follow
the same tenancy rules as the API.
