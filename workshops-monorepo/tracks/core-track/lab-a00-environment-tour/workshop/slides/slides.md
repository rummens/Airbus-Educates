<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Your Workshop Environment

A short tour of the environment every DCS Academy lab runs in, so the tools never get in the way of the learning.

**In this lab:** the dashboard layout · the split terminal · the editor · the Console (Kubernetes Dashboard) · the feedback form.

Digital Container Service · DCS Academy

---

<!-- id: dashboard-layout -->
## The Dashboard Layout

Every lab uses the same two-part screen: instructions on the left, a work area of tabs on the right. Learn it once and every lab looks the same.

- **Left — Instructions.** The lab content you read and click through.
- **Right — Work area.** Tabs (Terminal, Editor, Console); one visible at a time.
- Three clickable actions: **run a command**, **edit a file**, **verify**.
- **Verify** boxes are examiner tests: they inspect the cluster and turn green only when a step really worked.
- A red check means fix the step before moving on; the checks are safe to re-run.

![DCS Academy workshop dashboard](dashboard-layout.svg)

---

<!-- id: terminal -->
## The Terminal

The Terminal tab is a shell in your DCS session, split into two panes so a lab can watch one thing while changing another. Every command uses `oc`, the OpenShift command line.

- **Upper** pane is `execute-1` (session 1, the default); **lower** is `execute-2` (session 2).
- A "run a command" action targets the right pane for you.
- `oc whoami` prints your identity, proving the session is already logged in.

```
oc whoami
```

Expected: your username. `oc status` (lower pane) shows your project is empty for now.

---

<!-- id: editor -->
## The Editor

The Editor tab is a full VS Code editor opened on your `~/exercises` folder. Labs use it to show a file and to edit one, always through clickable actions so you see the change happen.

- Scoped to `~/exercises`, not your whole home directory.
- An "edit a file" action opens the file and makes the change for you.
- Here you only open a file; there is nothing to edit yet.

```
editor:open-file  ~/exercises/README.md
```

Expected: the Editor tab switches into view showing `README.md`.

---

<!-- id: console -->
## The Console

The Console tab is a visual view of your namespace — the **Kubernetes Dashboard**. When a lab creates something from the terminal, you can switch here to see it laid out visually.

- It shows **your** namespace only; it is empty until you deploy something (from A01).
- It is **not** the OpenShift web console — that refuses to embed and is toured in the Console track.
- The tab runs as your session service account, enough for a quick visual check.

Open it pointed at your own namespace with a `reload-dashboard` action; no login needed.

---

<!-- id: close -->
## You're ready

You now know the dashboard, the two terminal panes, the editor, the Console tab, and the feedback form — everything the real labs use.

**Next:** *What is DCS?* — the first concept lab, before you deploy your first app.
