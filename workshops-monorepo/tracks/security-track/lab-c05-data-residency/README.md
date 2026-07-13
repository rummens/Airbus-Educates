# EU Data-Residency & Compliance

**Look at DCS through a governance lens: how it classifies data, how it guarantees data stays in the right European region, and how workload placement is expressed and governed.**

The Digital Container Service (DCS) runs on-prem and air-gapped across a multi-national European footprint (for example Germany and Spain) — which is exactly what makes a data-residency guarantee possible: if data physically cannot leave the platform, keeping it in a permitted region becomes a structural property, not a promise on paper. Where the earlier Security labs hardened the image and the runtime, this one places what you run inside the EU data-residency frame. It is mostly concept and observe: you'll read governance artefacts and inspect how placement is declared, rather than deploy anything.

- **Track:** Security & Compliance — Secure on DCS · Lab 5 of 5
- **Audience:** Intermediate — know the Tenant → Namespaces model and comfortable with `oc get` and `jsonpath`
- **Duration:** ~35 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** the Core track (especially tenancy & quotas); familiar with labels/selectors and `nodeSelector`.

## By the end of this lab you'll be able to

- Explain the DCS Data Classification scheme and the multi-national data-residency guarantee that pins each classification to permitted region(s).
- Describe how workload placement is expressed — standard region/zone labels plus `nodeSelector` — and inspect it in a manifest.
- Read the Responsibility Matrix (RACI) to tell platform duties from tenant duties.
- Describe the Security Exception Process and the Terms & Conditions governing data and registry use.
- Identify the tenant compliance loop: classify data, tag and place the workload, request an exception via ITSM when a control can't be met.

## What you'll do

- Read the DCS data-classification matrix and the residency guarantee it pins to each level.
- Inspect a classified workload manifest to see how region labels and `nodeSelector` express placement.
- Walk the Responsibility Matrix and the ITSM exception process, then trace the full tenant compliance loop — all against read-only governance fixtures.
