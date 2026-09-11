---
title: Move the Credential to a Secret
---

Now the fix. You'll put the token in a dedicated **Secret**, then wire a new deployment to
read it **by reference** — so the literal never appears in the workload's manifest.

## Create the Secret

Open the Secret manifest:

```editor:open-file
file: ~/exercises/secret.yaml
```

Notice it uses `stringData`, not `data`:

```yaml
stringData:
  api-token: "s3cr3t-plaintext-token"
```

`stringData` is the author-friendly form: you write the value in plaintext and Kubernetes
base64-encodes it into `.data` for you when the object is stored. (You could instead run
`oc create secret generic app-secrets --from-literal=api-token=...`; the manifest is used
here so the object is inspectable in the editor.)

Apply it:

```terminal:execute
command: oc apply -f secret.yaml
```

```examiner:execute-test
name: verify-secret-exists
title: The app-secrets Secret exists with key api-token
args:
- app-secrets
- api-token
timeout: 15
```

{{< note >}}
Remember page 1: writing the token here has **not** encrypted it — `stringData` is just
encoded on storage. What changed is *where* it lives. The value is now behind the `secrets`
RBAC verb and covered by etcd encryption at rest, instead of sitting in a Deployment that
`get deploy` exposes.
{{< /note >}}

## Reference the Secret from the workload

Open the fixed Deployment:

```editor:open-file
file: ~/exercises/deploy-fixed.yaml
```

The `env` block no longer holds a value — it points at the Secret:

```yaml
        env:
        - name: API_TOKEN
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: api-token
```

The container still gets an `API_TOKEN` environment variable at runtime, but the manifest
carries only a **reference** — the name of the Secret and the key to read. No literal. Nothing
to leak into git or an env dump.

Apply it and wait for the rollout:

```terminal:execute
command: envsubst < deploy-fixed.yaml | oc apply -f -
```

```terminal:execute
command: oc rollout status deploy/fixed-app --timeout=60s
```

```examiner:execute-test
name: verify-fixed-running
title: The fixed deployment rolled out
args:
- fixed-app
timeout: 120
retries: .INF
delay: 3
```

{{< note >}}
If the Secret were missing or the key misnamed, the pod would never start — it would stall in
`CreateContainerConfigError`. A green rollout here means the reference resolved correctly.
{{< /note >}}

The token is now sourced by reference. On the next page you'll prove it's no longer exposed.
