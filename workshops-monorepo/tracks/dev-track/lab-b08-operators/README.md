# Operators on DCS

**The Developer track capstone: how DCS delivers whole platform services, not just your own apps.**

Everything so far has been resources you fully own — Deployments, ConfigMaps, your own
image builds. This lab introduces a different shape: the **Operator pattern**, where a
controller installed by the platform watches a Custom Resource you create and drives a
whole application (here, a PostgreSQL database) toward the state you asked for. You'll
inspect the operator's CRDs, create a real instance, watch it reconcile, and then learn
the DCS-specific split that matters most in practice — the platform owns the operator,
you own the instance it manages.

- **Track:** Developer · Lab 8 of 8 (capstone)
- **Audience:** Advanced — you've completed the Developer track through RBAC & Tenancy
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** lab-b05-rbac-tenancy; comfortable reading Kubernetes YAML and `oc get`/`describe` output

## By the end of this lab you'll be able to

- Explain the Operator pattern: a controller that reconciles a Custom Resource toward its desired state.
- Distinguish a CRD (a new resource *type*) from a CR (an *instance* of that type).
- Explain OLM and OperatorHub at a high level, and why DCS's OperatorHub is curated and air-gapped.
- State the DCS ownership model: the platform installs and updates the operator; you own and operate the instance it manages.
- Create a Custom Resource, watch the operator reconcile it, and read its status.

## What you'll do

Inspect the CRDs and API resources an already-installed operator adds to the cluster,
apply a small CloudNativePG `Cluster` custom resource, watch the operator provision it
from an empty status to a healthy running database, and then work through what that
means for who is on the hook when something goes wrong — you, not DCS support.

## Before you start

This lab reuses the **CloudNativePG** operator as a teaching example — the same one
used later, in depth, by the dedicated **Operators / Platform Services** track (GitLab,
Argo CD, CloudNativePG). This lab stays at the pattern and ownership level; it does not
duplicate that track's depth.
