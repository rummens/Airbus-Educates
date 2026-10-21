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

```examiner:execute-test
name: verify-prod-route-host
title: Verify the Route host follows the platform's DNS pattern
timeout: 30
retries: .INF
delay: 3
```

The Route YAML is identical; only the namespace type differs. One policy, reading one label,
made both decisions.
