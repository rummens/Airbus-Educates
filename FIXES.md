# DCS Academy — what changed

Copy-paste-into-chat log of learner-visible fixes and improvements. Newest day first,
one line per change, no internals. Platform/portal changes are live once ArgoCD has
synced `main`; workshop content is live on the next session start.

## 2026-08-13

- Core track order: **What is DCS?** now comes second, right after the environment tour, so you get the platform introduction before the hands-on labs. It is still optional — you can skip ahead to Deploy Your First App and come back.
- Lab pages no longer carry fixed "Lab 4"-style numbers that disagreed with the catalog; the catalog does the numbering.
- Storage lab: writing the marker file into the mounted volume works now — it failed with "Permission denied" before.
- All labs: cross-references use lab names ("the Expose Your App lab") instead of internal codes like A01 / B06, so they match what the catalog shows.
- Verify buttons no longer turn green before you have done the step: the checks that used to pass on things the platform provides (your session, your namespace, the peer namespaces, the storage classes, the network policy, the blocked internet access) now check *your* command output.
- Verify buttons: an amber button means it is queued behind another check, not broken — the first lab now says so. Checks that wait for a rollout retry by themselves instead of showing red.
- Configure & Troubleshoot: the broken-Pod page now shows the failing Pod's events (the old one was hiding them), and the logs step tells you the error message you actually get.
- What is DCS: says plainly that DCS is the platform of Airbus Defence and Space.
- Terms — Namespaces & Tenancy: new office-building analogy for Tenant, Namespace, RBAC and PROD.
- Expose Your App: links now say when they point at OpenShift documentation.
- Catalog: a lab you rated shows your rating right away, marked "provisional" until enough people have rated it.
- Console lab "Diagnose a broken pod": the lab starts again. The launch screen was waiting for the deliberately broken pod to become healthy — which it never does, because fixing it is the exercise.
- Console labs: a new **Exit lab** button next to Stop takes you back to the Academy — before, stopping the guidance left you with no way out. The blue highlight pulses once instead of three times.

## 2026-07-31

- Catalog: lab ratings now show the score as a number and the stars are filled in — you can actually see 4 stars vs 5.
- Trophies page: each earned trophy can be downloaded as a PNG badge (mail signature, chat profile).
- Lab A00 (Your Workshop Environment): new second page **Quick Actions** — the clickable boxes are explained and tried once each before the rest of the lab uses them.
- Lab A00: dashboard picture and slides updated — tab order matches the real dashboard and the **Feedback** tab is shown.
- Lab A00: the "not the OpenShift console" explanation on the Console page is cut down to two sentences; the harmless permission warnings in the empty Console are now mentioned so they don't look like a fault.
- All labs: the "first time here?" link on page 1 now points at the Academy **Help** page instead of a DCS docs URL that did not resolve.
- Wording pass across A00–A07 to drop stock phrasing.
- Admin: the comment pop-up has a **Copy** button.
- Catalog repo: the README is now a plain map of the labs for readers; the chart/deploy detail moved to a separate developer page.
