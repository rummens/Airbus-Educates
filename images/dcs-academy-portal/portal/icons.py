"""Vendored inline SVG line-icons (24x24, stroke-based, teal via currentColor).

Values are the *inner* markup of an <svg>; app._icon wraps them. Track.spec.icon
and difficulty map to these names. No external icon font/CDN.
"""
ICONS = {
    "dot": '<circle cx="12" cy="12" r="2.5"/>',
    "layers": '<path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    "cog": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1Z"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/>',
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
    "trending-up": '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v2M15 2v2M9 20v2M15 20v2M2 9h2M2 15h2M20 9h2M20 15h2"/>',
    "check-circle": '<path d="M22 11.1V12a10 10 0 1 1-5.9-9.1"/><path d="m9 11 3 3L22 4"/>',
    "file-check": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "signal": '<path d="M4 20v-4M9 20v-8M14 20v-12M19 20V4"/>',
    "star": '<path d="M12 2 15 9l7 .6-5.3 4.6L18.2 21 12 17.3 5.8 21l1.5-6.8L2 9.6 9 9Z"/>',
    "trophy": '<path d="M8 21h8"/><path d="M12 17v4"/><path d="M7 4h10v5a5 5 0 0 1-10 0Z"/><path d="M7 6H4v2a3 3 0 0 0 3 3"/><path d="M17 6h3v2a3 3 0 0 1-3 3"/>',
    "medal": '<circle cx="12" cy="15" r="5"/><path d="M12 13v4M10.5 15h3"/><path d="M8.5 8 6 3h4l2 3M15.5 8 18 3h-4l-2 3"/>',
    "award": '<circle cx="12" cy="9" r="5"/><path d="M9 13.5 7.5 21 12 18l4.5 3L15 13.5"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2 0-2.8a2 2 0 0 0-3 .8Z"/><path d="M12 15 9 12c.5-3 2-6 8-9 .3 6-2.7 7.5-5 8Z"/><path d="M9 12H4s.5-3 3-4c1.5-.6 3 0 3 0"/><path d="M12 15v5s3-.5 4-3c.6-1.5 0-3 0-3"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m13 5 7 7-7 7"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5Z"/>',
    "sparkles": '<path d="M12 3 13.5 9 19.5 10.5 13.5 12 12 18 10.5 12 4.5 10.5 10.5 9Z"/>',
    "help": '<circle cx="12" cy="12" r="9"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 2.5-3 4"/><circle cx="12" cy="17.5" r=".6" fill="currentColor" stroke="none"/>',
    "terminal": '<path d="m4 17 6-5-6-5"/><path d="M12 19h8"/>',
    "monitor": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    "edit": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
    "list-checks": '<path d="m3 7 2 2 3-3"/><path d="m3 17 2 2 3-3"/><path d="M13 8h8M13 16h8"/>',
    # topic icons for per-course logos
    "box": '<path d="M21 8 12 3 3 8v8l9 5 9-5Z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
    "boxes": '<path d="M7 3 3 5v4l4 2 4-2V5Z"/><path d="M17 3l-4 2v4l4 2 4-2V5Z"/><path d="M12 12l-4 2v4l4 2 4-2v-4Z"/>',
    "network": '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M12 11.5 6.5 17M12 11.5 17.5 17"/>',
    "hard-drive": '<path d="M4 13h16"/><path d="M6.5 5h11l3 8v5a1 1 0 0 1-1 1H4.5a1 1 0 0 1-1-1v-5Z"/><circle cx="8" cy="16.5" r=".6" fill="currentColor" stroke="none"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "key": '<circle cx="7.5" cy="15.5" r="3.5"/><path d="m10 13 8-8M15 5l3 3M13 7l2 2"/>',
    "server": '<rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/>',
    "cloud": '<path d="M17.5 18a4 4 0 0 0 .5-8 6 6 0 0 0-11.5 1.5A3.5 3.5 0 0 0 7 18Z"/>',
    "package": '<path d="M21 8 12 3 3 8v8l9 5 9-5Z"/><path d="m7.5 5.5 9 5M3 8l9 5 9-5M12 13v8"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.5 6 3.5 9s-1 6.5-3.5 9c-2.5-2.5-3.5-6-3.5-9s1-6.5 3.5-9Z"/>',
    "git-branch": '<circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="8" r="2.5"/><path d="M6 8.5v7M15.5 8.5C11 9 8.5 11 8.5 15.5"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 21c0-3.6 2.7-5.5 6-5.5s6 1.9 6 5.5"/><path d="M16 5.2a3.2 3.2 0 0 1 0 5.6M21 21c0-2.6-1.3-4.3-3.5-5"/>',
    "gauge": '<path d="M12 14 16 9"/><circle cx="12" cy="13" r="8"/><path d="M12 13h.01"/>',
    "route": '<circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.5 19H14a3.5 3.5 0 0 0 0-7H10a3.5 3.5 0 0 1 0-7h5.5"/>',
    "shield-check": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
}

# Font-Awesome-ish names → our vendored icon set (air-gapped: only these render).
ICON_ALIASES = {
    "cube": "box", "cubes": "boxes", "network-wired": "network",
    "diagram-project": "network", "sitemap": "network",
    "database": "database", "hard-drive": "hard-drive", "hdd": "hard-drive",
    "lock": "lock", "key": "key", "user-lock": "lock", "shield-halved": "shield",
    "server": "server", "cloud": "cloud", "docker": "box", "layer-group": "layers",
    "code": "code", "terminal": "terminal", "gears": "cog", "gear": "cog",
    "globe": "globe", "route": "route", "diagram-successor": "route",
    "users": "users", "gauge": "gauge", "gauge-high": "gauge", "book": "book",
    "circle-check": "check-circle", "code-branch": "git-branch",
}


def resolve_icon(name, default="book"):
    """Map an authored (possibly FA-style) icon name to a vendored icon key."""
    if not name:
        return default
    n = name.strip().lower().removeprefix("fa-")
    if n in ICONS:
        return n
    return ICON_ALIASES.get(n, default)


# difficulty → icon name (VM-world → k8s complexity signal)
DIFFICULTY_ICON = {
    "beginner": "signal", "intermediate": "signal",
    "advanced": "signal", "extreme": "signal", "": "signal",
}
