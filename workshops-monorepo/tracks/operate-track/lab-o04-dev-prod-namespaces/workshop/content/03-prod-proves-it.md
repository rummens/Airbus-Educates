---
title: PROD Makes You Prove It
---

Now apply the same manifest to the PROD namespace.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/prod
```

## Apply the unsized manifest to PROD

```terminal:execute
command: envsubst < hello-dcs-unsized.yaml | oc apply -f - -n $PROD_NS || true
```

```section:begin
name: breakdown-unsized-prod
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < hello-dcs-unsized.yaml`** — reads the same unsized manifest and replaces `${DCS_REGISTRY}` with its value from your session.
- **`| oc apply -f - -n $PROD_NS`** — the pipe hands that output to `oc apply`; `-f -` reads the manifest from the pipe, and `-n $PROD_NS` applies it in the PROD namespace.
- **`|| true`** — the refusal is expected; this keeps the step from being marked as failed.

```section:end
name: breakdown-unsized-prod
```

PROD refuses it. Read the message before you change anything:

```
PROD requires every container to declare CPU and memory requests and limits.
rule autogen-prod-requires-resources failed at path
/spec/template/spec/containers/0/resources/limits/
```

```examiner:execute-test
name: verify-prod-rejects-unsized
title: Verify PROD refused the unsized workload
timeout: 30
retries: .INF
delay: 3
```

Three things in that message:

- it names the **rule** (`prod-requires-resources`);
- it names the **path** that failed, down to the container index;
- it happened at **`oc apply`**, so nothing was created and nothing started and failed
  later.

{{< note >}}
**📌 Why "autogen".** The rule is written against `Pod`, and the policy engine derives the
equivalent rule for the Deployment that would create the Pod. That is why the refusal comes
now, rather than as a healthy-looking Deployment that produces no Pods.
{{< /note >}}

## Fix the manifest, not the namespace

```editor:open-file
file: ~/exercises/hello-dcs-sized.yaml
```

The only difference from the refused file is the `resources` block: requests and limits on the
one container.

```terminal:execute
command: envsubst < hello-dcs-sized.yaml | oc apply -f - -n $PROD_NS && oc rollout status deploy/hello-dcs -n $PROD_NS --timeout=120s
```

```section:begin
name: breakdown-deploy-prod
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < hello-dcs-sized.yaml`** — reads the file and replaces `${DCS_REGISTRY}` with its value from your session, so the registry host is not hard-coded.
- **`| oc apply -f - -n $PROD_NS`** — the pipe hands that output to `oc apply`; `-f -` means "read the manifest from the pipe", and `-n $PROD_NS` applies it in that namespace.
- **`&&`** — runs the next command only if the one before it succeeded.
- **`oc rollout status deploy/hello-dcs -n $PROD_NS --timeout=120s`** — waits until the Deployment's Pods are ready, or gives up after 120 seconds.

```section:end
name: breakdown-deploy-prod
```

```examiner:execute-test
name: verify-prod-accepts-sized
title: Verify PROD accepted the sized workload
timeout: 90
retries: .INF
delay: 3
```

PROD admits it. The policy only requires the workload to declare its CPU and memory before it
runs.

## Publish it, from here

```terminal:execute
command: oc apply -f service.yaml -n $PROD_NS && oc apply -f route.yaml -n $PROD_NS
```

```section:begin
name: breakdown-publish-prod
prefix: Breakdown
title: What each part of the command does
```

- **`oc apply -f service.yaml -n $PROD_NS`** — creates the Service in the PROD namespace.
- **`&&`** — runs the next command only if that succeeded.
- **`oc apply -f route.yaml -n $PROD_NS`** — creates the same Route that DEV refused, this time in PROD.

```section:end
name: breakdown-publish-prod
```

```examiner:execute-test
name: verify-prod-route-created
title: Verify the Route was admitted in PROD and has a host
timeout: 60
retries: .INF
delay: 3
```

The identical Route manifest that DEV refused is admitted here, and the platform gives it a
real hostname:

```terminal:execute
command: oc get route hello-dcs -n $PROD_NS -o jsonpath='{.spec.host}{"\n"}'
```

```section:begin
name: breakdown-route-host
prefix: Breakdown
title: What each part of the command does
```

- **`oc get route hello-dcs -n $PROD_NS`** — reads the Route in the PROD namespace.
- **`-o jsonpath='{.spec.host}{"\n"}'`** — prints only the hostname the platform assigned, followed by a newline.

```section:end
name: breakdown-route-host
```

```examiner:execute-test
name: verify-prod-route-host
title: Verify the Route host follows the platform's DNS pattern
timeout: 30
retries: .INF
delay: 3
```

The Route YAML is identical; only the namespace type differs. One policy, reading one label,
made both decisions.
