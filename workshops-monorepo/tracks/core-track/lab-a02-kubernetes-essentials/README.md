# Kubernetes Essentials on DCS

**Deploy a real application, then take it apart to see how Kubernetes runs it.**

Every DCS project is built from the same handful of Kubernetes objects. In this lab you
deploy a working application and then inspect it layer by layer — Deployment, ReplicaSet,
Pod, and Service — learning not just the commands but *what* each object is, *why* it
exists, and *how* the pieces fit. You'll also watch Kubernetes self-heal a deleted Pod and
give your app a stable in-cluster address.

- **Track:** Core — DCS Foundations · Lab 2 of 9
- **Audience:** Beginner to intermediate — comfortable at the `oc` command line
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-a01-what-is-dcs

## By the end of this lab you'll be able to

- Choose between imperative and declarative resource management, and preview changes with `--dry-run`.
- Create and manage a Deployment, and explain how it owns ReplicaSets and Pods.
- Use labels and selectors to identify and query resources.
- Inspect resources with `oc get`, `oc describe`, and `oc explain`.
- Scale a Deployment and watch Kubernetes self-heal a deleted Pod.
- Read logs and exec into a running container to debug.
- Give an application a stable address with a Service and reach it in-cluster by DNS.

## What you'll do

You'll deploy the `hello-dcs` sample app, then work through it hands-on: create resources
imperatively and declaratively, query them by label, scale the Deployment up and down,
delete a Pod and watch it come back, read logs, exec into a container, and finally front it
with a Service you reach by DNS.
