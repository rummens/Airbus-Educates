---
title: The Editor
---

The **Editor** tab is a full [VS Code](https://code.visualstudio.com/) editor, opened on
your `~/exercises` folder.

Labs use it for two things:

- to **show** you a file — a manifest, a config;
- to **edit** one — always through a clickable action, so you watch the change happen
  instead of typing it.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/editor
```

## Open a file

Click the box below. It switches to the Editor tab and opens the welcome file in your
exercises folder:

```editor:open-file
file: ~/exercises/README.md
```

The Editor tab is now showing `README.md`.

In a real lab, an **edit a file** action highlights a line and changes it for you — insert,
replace, or append — so you see exactly what changed.

Here there is nothing to edit. This page only shows you where files open.

{{< note >}}
**📌 Note:** the editor only shows the `~/exercises` folder, not your whole home directory,
so you are never distracted by files a lab does not use.
{{< /note >}}

When you're done looking, switch back to the terminal:

```dashboard:open-dashboard
name: Terminal
```
