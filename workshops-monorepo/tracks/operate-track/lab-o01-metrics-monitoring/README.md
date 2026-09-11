# Metrics & Monitoring

**The platform already measures your Pods. It cannot measure what your app is doing unless the
app says so.**

CPU, memory and restarts come for free, and they answer "is this Pod healthy" — never "are
requests failing".

You expose metrics from the app, read the exposition format it serves, then ask to be scraped
with a **ServiceMonitor** — and check its selector really matches, because a ServiceMonitor
that matches nothing looks exactly like one that works.

Then you query your own series back with **PromQL**, from the terminal, through the platform's
tenant query endpoint.

The last step is the one worth remembering: ask about your namespace and you get an answer;
ask about somebody else's and you get **Forbidden**. Tenancy is enforced in the metrics path
too.

> **💡 Tip:** you never configure Prometheus here. You put one object in your own namespace and
> the platform's monitoring finds it.

- **Track:** Operate & Observe
- **Audience:** Intermediate
- **Duration:** ~25 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
- **Prerequisites:** **Services & Cluster Networking** (a ServiceMonitor selects a Service, by label and port name). Helpful: **Health & Resources**.

## By the end of this lab you'll be able to

- Explain the path a metric takes from your container to a query, and who owns each hop.
- Read the Prometheus exposition format your app serves.
- Create a ServiceMonitor and confirm it is actually selecting something.
- Query your series with `rate()` and `sum by`.
- Explain why the same query about another namespace is refused.

## What you'll do

1. **Deploy** the app and look at what it exposes.
2. **Generate** traffic and watch the counter move.
3. **Ask** to be scraped, and verify the selector matches.
4. **Query** your own metrics, then ask a real question with PromQL.
5. **Get refused** asking about a namespace that is not yours.
