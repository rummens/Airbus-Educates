# DEV vs PROD Namespaces

**Two namespaces, the same manifest, two different answers.**

DEV and PROD on DCS are not separated by a naming convention. They differ in **policy
posture**: PROD enforces rules DEV does not, and only PROD may publish a **Route**.

This session gives you one of each. You apply the same unsized Deployment to both and watch
PROD refuse it — at `oc apply`, with the failing field named. Then the same Route to both, and
watch DEV refuse that one.

Neither refusal is a bug, and neither is simulated: you read the real admission policy that
produced them.

Ends on **promotion** — why the answer is a fresh apply to PROD rather than an edit in place,
and where the image has to come from.

> **💡 Tip:** the error messages are the lesson here. Read them before you fix anything.

- **Track:** Operate & Observe
- **Audience:** Intermediate
- **Duration:** ~25 min
- **Format:** Hands-on, guided — split terminal + editor, with three namespaces: your session's, plus a DEV and a PROD one
- **Prerequisites:** Core **Terms — Namespaces & Tenancy** and **Health & Resources** (PROD is about to insist on requests and limits).

## By the end of this lab you'll be able to

- Say what actually distinguishes a DEV namespace from a PROD one.
- Predict which manifests PROD will refuse, and why.
- Read an admission rejection and find the rule behind it.
- Explain why only PROD may publish a Route.
- Describe promotion, and why it is not an edit in place.

## What you'll do

1. **Read** the label and the policy that reads it.
2. **Deploy** something unfinished to DEV, as intended.
3. **Fail** to publish it from DEV.
4. **Fail** to deploy it to PROD, and read why.
5. **Size** it, get it admitted, and publish from PROD.
6. **Compare** both environments, and name what promotion means.
