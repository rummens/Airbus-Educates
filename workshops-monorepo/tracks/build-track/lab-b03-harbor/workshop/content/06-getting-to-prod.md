---
title: Getting an Image Into PROD
---

You have a built image in a DEV project, and a PROD project that refuses pushes. There are
two routes in.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/promotion
```

## Route 1: take something already cleared

The **green catalog** holds images that have already been reviewed, scanned and signed off.
If what you need is there, use it rather than build a near-identical one.

A base image from the green catalog also makes your **own** builds more likely to pass the
gate, because you inherit its clean starting point.

## Route 2: promote your own image

A mirror from the DEV project into the PROD project, which is the `skopeo copy` you ran
earlier, with three differences:

1. **You do not run it.** It is requested through **ITSM** and the platform performs it.
   Self-service is the direction; a ticket is where it stands today.
2. **The image must pass the gate**, below the CVE threshold, or the destination will not
   serve it.
3. **The digest is preserved**, so what was scanned and what runs are provably the same
   bytes.

{{< note >}}
**📌 Why not just let teams push to PROD?** "No pushes" is a stronger guarantee than "pushes
that are checked". It means there is no path at all to a production image that skipped the
review, including by accident.
{{< /note >}}

## Robot accounts

Neither route uses your personal login. Registry credentials for automation are **robot
accounts**, issued to a system, scoped to one project and revocable on their own.

Two consequences you feel directly:

- a pipeline keeps working when you change your password or leave the team;
- a leaked credential is scoped to one project's push rights, not to everything you can
  reach.

## Putting the whole track together

You can now follow one artefact end to end:

1. **Build** it on the cluster, with no daemon (*Build Your Image*).
2. It lands in your **DEV project**, which takes the push without complaint.
3. It is **scanned**, and the report says whether it can go further.
4. It is **promoted** into PROD by mirror, or replaced by something from the green catalog.
5. It is deployed into a **PROD namespace**, which enforces its own policies
   (*DEV vs PROD Namespaces*).

You control step 1. Steps 2 to 4 are the platform's checks on it.
