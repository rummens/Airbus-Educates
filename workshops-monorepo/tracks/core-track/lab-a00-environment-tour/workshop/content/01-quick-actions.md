---
title: Quick Actions
---

Before anything else, the one thing that makes these labs work: the **boxes** in the
instructions on the left. They are buttons. Click one and it does the work for you — types
a command, opens a file, checks your cluster, opens a slide. You rarely type anything by
hand.

If you skip past them and read only the text, the lab will feel broken. So try them here,
on a page where nothing can go wrong.

## The four kinds of box

| Box | What clicking it does |
|---|---|
| **Run a command** | Types the command into the terminal and runs it. |
| **Open or edit a file** | Opens the file in the editor, and makes the edit for you. |
| **Verify** | Runs a check against the cluster and turns green if the step worked. |
| **Open a tab** | Switches the right-hand side to the Terminal, Editor, Console or Slides. |

Everything a box does happens on the **right-hand side** of the screen. That is the
other half of the layout, and the next page walks through it.

## Try a "run a command" box

Click the box below once. Watch the right-hand side: it switches to the terminal, types
the command, and runs it.

```terminal:execute
command: echo "quick actions work" > ~/exercises/quick-actions.txt
```

The command writes one line into a file. There is no output — the shell prompt simply
comes back. That is normal for a command that redirects its output into a file.

## Try a "verify" box

Now the check. Click it: it looks for the file you just wrote and turns **green** if it is
there.

```examiner:execute-test
name: verify-quick-action
title: Verify your first quick action ran
timeout: 10
```

Green means the step really worked — not "the page scrolled past", but "the cluster and
your session are in the state this step promised". If a check is ever **red**, fix the
step above before moving on; checks are safe to click again.

{{< note >}}
**Amber means waiting, not broken.** Checks run one at a time. Click a second check while
the first is still running and it turns amber until its turn comes — then it runs and shows
its real result. Nothing is wrong; give it a moment.
{{< /note >}}

## Try an "open a file" box

Click below to open the file you just created in the editor:

```editor:open-file
file: ~/exercises/quick-actions.txt
```

The right-hand side switches to the Editor tab, showing your one line of text.

## Getting back

The right-hand side shows **one tab at a time**, so an action that opens the Slides or the
Editor pushes the terminal out of view. Nothing is lost — click the **Terminal** tab
header, or a box like this one:

```dashboard:open-dashboard
name: Terminal
```

{{< note >}}
**If a box seems to do nothing**, click it again. A "run a command" box needs the Terminal
tab; if you are looking at the Slides or the Editor, the command still ran — switch back to
the Terminal to see it.
{{< /note >}}

## One more: the slides

Each page has a slide with the same content in one picture. Clicking the box below opens the
**Slides** tab — and now you know how to get back:

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/quick-actions
```

```dashboard:open-dashboard
name: Terminal
```
