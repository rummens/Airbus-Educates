---
title: Change & Run
---

A workspace is only useful if you can change code and see the result. Do exactly that — inside
the cluster.

{{< note >}}
The commands below run in the **workspace terminal** (inside Dev Spaces), *not* this session's
Educates terminal. In concept mode, read them as the steps you'd take in the IDE.
{{< /note >}}

## Edit, run, see it

1. In the Dev Spaces editor, open the sample app's source and change the response text (for
   `hello-dcs`, the served page/string).
2. Run the app with the devfile's **run** command (the IDE surfaces it as a task, or in the
   workspace terminal):

   ```
   python3 -m http.server 8080
   ```

3. Open the exposed **8080** endpoint (Dev Spaces offers a link when the port opens). You see
   your change served **live, from inside the cluster** — no build pipeline, no redeploy.

## Compare with B01

In B01 your loop was: edit a manifest → `oc apply` → `oc rollout status` → check. That deploys
a **built image**. Here the loop is: edit source → run in the workspace → refresh. That's the
**inner** development loop — fast iteration on code — and it happens *on the platform*, under
the same policies as production.

Both matter: you iterate in Dev Spaces, then deploy the built image with the skills from B01.

## Check Your Understanding

You changed a string and saw it immediately without `oc apply`. Why didn't you need to
rebuild and redeploy an image?

{{< note >}}
**Answer:** The workspace runs your **source** directly with the devfile's run command — the
inner loop. Building an image and `oc apply` is the outer loop you use to *deploy* the finished
change (B01).
{{< /note >}}
