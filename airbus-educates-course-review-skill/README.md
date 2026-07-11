# Airbus Educates Course Review Skill

A Claude Code skill that reviews DCS Academy Educates workshops/courses against
the house standards defined by the `airbus-educates-workshop-authoring` and
`airbus-educates-course-design` skills, and reports ranked findings with
concrete improvement suggestions.

It is the QA counterpart to those skills — they create, this one checks and
advises (it does not rewrite unless separately asked).

## Usage

```
/airbus-educates-course-review
```

Or ask Claude to "review / audit / QA this workshop (or course) against our
rules" or "how can this workshop be improved?". Scope is a single workshop
(`workshops/lab-*`) or a whole course (`planning/` + all workshops).

See `SKILL.md` for the review process, severity levels, and the full rubric.
