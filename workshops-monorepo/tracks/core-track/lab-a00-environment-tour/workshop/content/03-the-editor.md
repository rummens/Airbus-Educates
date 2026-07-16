---
title: The Editor
---

The **Editor** tab is a full [VS Code](https://code.visualstudio.com/) editor, opened on
your `~/exercises` folder. Labs use it for two things: to *show* you a file (a manifest, a
config) and to *edit* one — always through clickable actions, so you can watch the change
happen instead of typing it.

## Open a file

Click the box below. It switches to the Editor tab and opens the welcome file in your
exercises folder:

```editor:open-file
file: ~/exercises/README.md
```

The Editor tab is now showing `README.md`. In a real lab, an "edit a file" action would
highlight a line and change it for you — insert, replace, or append — and you'd see
exactly what changed. Here there's nothing to edit; this is just to show you where files
open.

{{< note >}}
The editor only shows the `~/exercises` folder, not your whole home directory, so you're
never distracted by files a lab doesn't use.
{{< /note >}}

When you're done looking, switch back to the terminal:

```dashboard:open-dashboard
name: Terminal
```
