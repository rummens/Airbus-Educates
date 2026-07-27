---
title: The Native OpenShift Console
---

This PoC leaves the Educates dashboard and opens the real **OpenShift web console** in
the same browser tab. Educates cannot embed the console, but it can pass the namespace
allocated for this session, the dashboard return address, and a browser-history checkpoint
to the Academy console plugin.

## Open the console and start the tour

Click below. If the OpenShift login page appears, sign in with your normal cluster
identity. The Academy plugin then starts a short tour scoped to this session namespace.

{{< open-native-console >}}

{{< note >}}
The native console uses your browser login, not the Educates session service account.
For this PoC, Educates creates a namespace-local RoleBinding for that user when the
session is allocated. The tour receives the generated namespace name and an encoded
dashboard return URL. The history checkpoint lets the browser restore the current
instruction page and split dashboard layout.
{{< /note >}}

Follow the highlighted **Workloads** and **Pods** entries. The tour ends when the Pods
page for your Educates session namespace is open. Select **Return to Academy lesson**
to navigate this browser tab back to this page.
