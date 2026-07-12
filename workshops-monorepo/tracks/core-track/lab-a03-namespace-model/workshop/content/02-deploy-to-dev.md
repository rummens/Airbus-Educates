---
title: Deploy to DEV
---

Start where all work starts on {{< param product_short >}}: a **DEV** namespace, where you
can iterate freely.

## Create a DEV namespace

Open the manifest — it's an ordinary Namespace with one important label,
`dcs.airbus/namespace-type: dev`, which marks its lifecycle type:

```editor:open-file
file: ~/exercises/dev-namespace.yaml
```

Apply it:

```terminal:execute
command: oc apply -f dev-namespace.yaml
```

You should see `namespace/team-dev created`. Confirm the type label is set — this is what
tells the platform (and you) that it's a DEV namespace:

```examiner:execute-test
name: verify-ns-type
title: DEV namespace exists with the dev type label
args:
- team-dev
- dev
timeout: 10
```

## Deploy the sample app into DEV

Now deploy the same `hello-dcs` app you know from the previous workshop — this time
targeting the DEV namespace with `-n team-dev`:

```editor:open-file
file: ~/exercises/hello-dcs.yaml
```

Note this manifest has **no `data-classification` label**. In DEV that's fine — there's no
policy gate. Apply it:

```terminal:execute
command: oc apply -n team-dev -f hello-dcs.yaml
```

{{< note >}}
The Deployment needs to pull its image and start a Pod — give it a few seconds. "Done"
means the Deployment reports an available replica.
{{< /note >}}

```examiner:execute-test
name: verify-workload-ready
title: hello-dcs is running in the DEV namespace
args:
- hello-dcs
- team-dev
timeout: 90
retries: .INF
delay: 3
```

It ran without complaint — because DEV imposes no admission policy. Remember that: in the
next step you'll apply the *exact same manifest* to a PROD namespace and watch a very
different outcome.
