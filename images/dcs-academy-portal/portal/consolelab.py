"""Console labs — the UI-driven lab format.

A console lab reuses the whole Educates machinery (session namespace, quota,
`spec.session.objects` pre-deploying the resources, capacity, the reaper) but the
learner never opens the workshop dashboard. Once the session is allocated the
portal redirects the browser to the OpenShift console, where the academy console
plugin runs the guided lab against the session namespace.

The Workshop CR declares the format:

    metadata:
      labels:
        academy.dcs/lab-format: console          # terminal (default) | console
      annotations:
        academy.dcs/console-lab: lab-container-access
        academy.dcs/console-lab-params: podName=lab-app

`ns` is always injected by the portal from the allocated session namespace — a
lab never declares it. Extra params are static per lab and fill the remaining
`{{placeholders}}` of the ConsoleLab CR.
"""
import logging
import urllib.parse

log = logging.getLogger("portal.consolelab")

CONSOLE_FORMAT = "console"
DEFAULT_FORMAT = "terminal"

# Same contract as the console plugin's launch-parameter sanitizer: anything that
# can appear in a Kubernetes name or a console path, nothing that could smuggle
# markup or a second query parameter into the URL we build.
_NAME_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:/-@")
_RESERVED = {"ns", "mode", "returnUrl"}


def is_console_lab(course):
    return (course or {}).get("lab_format") == CONSOLE_FORMAT


def parse_params(annotation, session_namespace=""):
    """`podName=web,secondNamespace=other` → {"podName": "web", ...}.

    Invalid pairs are dropped with a warning rather than failing the launch: a
    typo in one annotation should not make the lab unlaunchable, and the console
    plugin already refuses to start a lab whose parameters are missing.

    A value may contain `$(session_namespace)`, the one Educates variable a lab
    author cannot resolve at authoring time: a secondary session namespace is named
    `$(session_namespace)-<suffix>` and the session namespace is only known once the
    session is allocated. It is substituted before validation, because the literal
    form contains characters the sanitizer rejects.
    """
    params = {}
    for pair in (annotation or "").split(","):
        pair = pair.strip()
        if not pair:
            continue
        key, sep, value = pair.partition("=")
        key, value = key.strip(), value.strip()
        if session_namespace:
            value = value.replace("$(session_namespace)", session_namespace)
        if not sep or not key or not value:
            log.warning("CONSOLE-LAB ignoring malformed param %r", pair)
            continue
        if key in _RESERVED:
            log.warning("CONSOLE-LAB ignoring reserved param %r", key)
            continue
        if not key.isalnum() or not set(value) <= _NAME_CHARS:
            log.warning("CONSOLE-LAB ignoring unsafe param %r", pair)
            continue
        params[key] = value
    return params


def launch_url(course, session_namespace, console_base, return_url=""):
    """The console URL that starts this lab in the learner's session namespace.

    Returns "" when the course is not a console lab, is missing its ConsoleLab
    reference, or we could not determine the console host — the caller then falls
    back to the normal Educates session redirect instead of sending the browser
    somewhere broken.
    """
    lab = (course or {}).get("console_lab", "")
    if not (is_console_lab(course) and lab and session_namespace and console_base):
        return ""
    params = parse_params(course.get("console_lab_params", ""), session_namespace)
    params["ns"] = session_namespace
    if return_url:
        params["returnUrl"] = return_url
    query = urllib.parse.urlencode(params)
    path = f"/academy/lessons/{urllib.parse.quote(lab, safe='')}/start"
    return f"{console_base.rstrip('/')}{path}?{query}"
