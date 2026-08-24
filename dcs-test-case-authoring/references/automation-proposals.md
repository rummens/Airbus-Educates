# Writing the Automation Proposal

The proposal is read by a test engineer who will implement it. It must name the tool
and enumerate the **asserts** — not "automate with Chainsaw", but which resource is
applied, which field is checked, and what the failure case is.

Rule of thumb: if the proposal does not say what makes the test go red, it is not
finished.

---

## `test::chainsaw` — Kyverno Chainsaw

Use for: applying a manifest and asserting the API server accepts, denies, or mutates
it. The natural fit for Kyverno policies, admission webhooks, provisioner CRs, quotas.

Step vocabulary: `apply`, `assert`, `error`, `command`, `script`, `delete`.

- `assert` — the resource exists with these fields (partial match).
- `error` — this resource must **not** exist / must not match. The negative half.
- `command` — shell out when a field check is not expressive enough.

Proposal wording:

> Chainsaw: `apply` the PVC fixture in `dcs-monitoring`, `assert`
> `status.phase: Bound`; then `apply` the same fixture in a tenant namespace and
> `error` on any PVC existing there. A `command` step runs
> `oc get events -o jsonpath=...` and asserts the denial message names the
> `require-storage-class` policy.

Skeleton the engineer will produce:

```yaml
apiVersion: chainsaw.kyverno.io/v1alpha1
kind: Test
metadata:
  name: pvc-storage-class
spec:
  steps:
    - name: allowed-in-platform-namespace
      try:
        - apply:
            file: pvc-with-sc.yaml
        - assert:
            resource:
              apiVersion: v1
              kind: PersistentVolumeClaim
              metadata:
                name: test-pvc
              status:
                phase: Bound
    - name: denied-without-storage-class
      try:
        - apply:
            file: pvc-no-sc.yaml
            expect:
              - check:
                  ($error != null): true
        - error:
            resource:
              apiVersion: v1
              kind: PersistentVolumeClaim
              metadata:
                name: test-pvc-no-sc
```

State the fixture file names in the proposal — the engineer should not have to invent
them.

---

## `test::robot` — Robot Framework

Use for: HTTP endpoints, UI logins, cluster queries via KubeLibrary, anything with a
status code or a returned field.

Name the keywords/libraries, the endpoint, and the expected status codes.

Proposal wording:

> Robot Framework with `KubeLibrary` and `RequestsLibrary`: authenticate to the Harbor
> API with the robot account, `GET /api/v2.0/projects/tenant-demo`, assert
> `cve_allowlist.items` contains the CVE and `expires_at` equals the requested date;
> then assert an anonymous `GET` on the same path returns `401`.

Skeleton:

```robotframework
*** Settings ***
Library    KubeLibrary
Library    RequestsLibrary

*** Test Cases ***
CVE Allowlist Exception Is Applied
    ${resp}=    GET    ${HARBOR}/api/v2.0/projects/tenant-demo    auth=${ROBOT_AUTH}
    Status Should Be    200    ${resp}
    Should Contain    ${resp.json()}[cve_allowlist][items]    ${CVE_ID}

Anonymous Access Is Rejected
    ${resp}=    GET    ${HARBOR}/api/v2.0/projects/tenant-demo    expected_status=401
```

---

## `test::python` — Python / pytest

Use for: logic too involved for Robot keywords, SDK or API client flows, set
intersections, parsing scan reports.

Name the client, the fixture, and the assertion.

> pytest with the Kubernetes client: list `NetworkPolicy` objects in every tenant
> namespace, assert each carries the baseline `deny-all` policy, and assert the count
> of namespaces missing it is `0`. Fixture creates two namespaces, one via the
> provisioner and one by hand, and expects only the provisioner one to comply.

---

## `test::helm-test` — chart test hook

Use for: a chart's own smoke test — the component came up and serves.

> Helm test hook in the chart: a Job that curls the service's `/healthz` and exits
> non-zero on anything but `200`. Runs as part of `helm test <release>` in the chart's
> CI job.

---

## `test::grafana`

Use for: a metric exists, a datasource is provisioned, a dashboard query returns data.

> Query the Thanos Querier for `up{cluster="de"}` over the last 15m and assert a
> non-empty result; assert the `grafana-sc-datasources` ConfigMap contains the Thanos
> datasource with `isDefault: false`; assert the dashboard UID is present via
> `GET /api/dashboards/uid/<uid>` returning `200`.

---

## `test::performance`

Use for: latency, throughput, resource ceilings. Always state the threshold, the load,
and the duration — a performance test without a number is not a test.

> Run 200 concurrent namespace provisioning requests for 10 minutes; assert p95
> reconcile time < 30s, zero failed reconciles, and controller memory below its limit
> throughout.

---

## `test::scenario`

No tool — a human-executed workflow. The proposal names which parts of it can later be
automated and with what:

> Manual for now. The blocked-action half (tenant cannot create a `ClusterRoleBinding`)
> is automatable with Chainsaw `error` steps once the tenant kubeconfig fixture exists.

---

## Checklist for any proposal

- [ ] Tool named, and it matches the `test::` label.
- [ ] The resource/endpoint/metric under test is named exactly.
- [ ] Each assert states the field and the expected value.
- [ ] The negative half is included where a boundary exists.
- [ ] Fixture files or test data are named, not implied.
- [ ] Thresholds are numeric where the test is about performance or timing.
