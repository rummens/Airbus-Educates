---
title: Catalogs, Projects and the Asymmetry
---

Three ideas, and the third one explains most of what people find surprising.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/rules
```

![Catalogs supply images the platform vouches for; a tenant namespace may get its own Harbor project, where DEV accepts pushes and PROD accepts none and pulls only below the CVE threshold; promotion into PROD is a mirror or the green catalog](registry-rules.svg)

## 1. Catalogs: where images come from

{{< param product_short >}} does not let a cluster pull from wherever a manifest points. Images
come from catalogs the platform curates:

- **the DCS catalog** — platform-provided images, mirrored and maintained.
- **allowed external** — upstream images that have been reviewed and mirrored in. Not
  "anything on the internet", a list.
- **proxy-cached** — a pull-through cache for sources that are permitted, so the cluster still
  never reaches out mid-deploy.
- **the green catalog** — images already **cleared** for production use. Golden, in the sense
  that somebody has signed off on them.

## 2. Projects: where *your* images go

A tenant may be given a **Harbor project of its own** — optional, and scoped **per namespace**
today. (A per-tenant model is the direction; the mapping is per-namespace for now.)

That project is where a build's output lands, and where your team's images live.

## 3. The asymmetry: DEV pushes, PROD does not

This is the rule to remember:

- **A DEV namespace's project takes pushes**, of anything. No CVE limitation. That is the
  point of DEV: iterate, push a broken image, push it again.
- **A PROD namespace's project takes no pushes at all.** And it pulls only images whose
  vulnerabilities are **below CVE severity 9**.

So you cannot build straight into production, by construction rather than by policy
enforcement after the fact.

{{< note >}}
**📌 If an image genuinely cannot meet the threshold** — an unfixable finding in a dependency
you need — there is a **security exception process**. It is a conversation with a decision at
the end of it, not a flag you set.
{{< /note >}}

## Prove the pull path works

```terminal:execute
command: envsubst < pod-from-registry.yaml | oc apply -f - && oc wait --for=condition=Ready pod/from-registry --timeout=180s
```

```examiner:execute-test
name: verify-pull-works
title: Verify your namespace can pull and run a registry image
timeout: 180
retries: .INF
delay: 5
```

Nothing exotic: this is every other lab's first step, seen as what it is — a **pull** from a
registry your namespace is allowed to pull from.

Next: look at an image without running it at all.
