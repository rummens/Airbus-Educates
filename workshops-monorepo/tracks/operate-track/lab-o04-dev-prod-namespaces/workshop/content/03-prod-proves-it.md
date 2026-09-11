---
title: PROD Makes You Prove It
---

Same manifest, different namespace. Watch what happens.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/prod
```

## Apply the unsized manifest to PROD

```terminal:execute
command: envsubst < hello-dcs-unsized.yaml | oc apply -f - -n $PROD_NS || true
```

**Refused** — and read the message before doing anything about it:

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

Three things worth noticing in that message:

- it names the **rule** (`prod-requires-resources`), so you can go and read it;
- it names the **path** that failed, down to the container index;
- it happened at **`oc apply`** — nothing was created, nothing started and failed later.

{{< note >}}
**📌 Why "autogen".** The rule is written against `Pod`, and the policy engine automatically
derives the equivalent rule for the Deployment that would create the Pod. That is why you are
refused now, rather than watching a healthy-looking Deployment produce no Pods.
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

Admitted. The policy was never asking for much — only that you say what the workload needs
before the platform commits to running it.

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

Same YAML. Same cluster. Different namespace type, different answer — and both answers came
from one policy reading one label.
