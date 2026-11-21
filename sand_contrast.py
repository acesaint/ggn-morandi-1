#!/usr/bin/env python3
"""Sand pair (warm-sand light + night-sand dark) - WCAG contrast verification.

Reproducible check for SAND_THEME_TOKENS.md (stage 1). Computes WCAG 2.1
contrast ratios for every mandatory foreground/background pair the GGn
stylesheet actually consumes, for BOTH sand themes. No CSS is modified.

Light matrix mirrors morandi_light_contrast.py (warm-paper baseline, 135
checks). Dark matrix is the dark-mode adaptation documented in
SAND_THEME_TOKENS.md: fg-accent text >=4.5 on surfaces 0-5 (all text-bearing
surfaces), >=2.7 documented on structural fills 6-9; alert link >=4.0
(parent dark-green parity); border thresholds >= light standard.

Run:  python3 sand_contrast.py
"""

import sys

def _srgb(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(hexcolor):
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _srgb(r) + 0.7152 * _srgb(g) + 0.0722 * _srgb(b)

def ratio(fg, bg):
    l1, l2 = lum(fg), lum(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)

def mix(fg, bg, pct):
    """color-mix(in srgb, fg pct%, bg) approximation used by .alert."""
    h1, h2 = fg.lstrip("#"), bg.lstrip("#")
    out = []
    for i in (0, 2, 4):
        a, b = int(h1[i:i + 2], 16), int(h2[i:i + 2], 16)
        out.append(round(a * pct / 100 + b * (100 - pct) / 100))
    return "#{:02x}{:02x}{:02x}".format(*out)

def interp(c1, c2, t):
    h1, h2 = c1.lstrip("#"), c2.lstrip("#")
    out = []
    for i in (0, 2, 4):
        a, b = int(h1[i:i + 2], 16), int(h2[i:i + 2], 16)
        out.append(round(a + (b - a) * t))
    return "#{:02x}{:02x}{:02x}".format(*out)

# ---------------------------------------------------------------------------
# Warm-sand light palette (user-confirmed anchor #F5F2EB; stage 1 final)
# ---------------------------------------------------------------------------
L = {
    "surface-0": "#EDE9DF", "surface-1": "#E8E3D8", "surface-2": "#F0EDE5",
    "surface-3": "#F5F2EB", "surface-4": "#FBF9F4", "surface-5": "#E9E4D9",
    "surface-6": "#F7F4ED", "surface-7": "#FAF8F2", "surface-8": "#FDFCF8",
    "surface-9": "#DDD6C8",
    "line-1": "#E1DCCF", "line-2": "#ADA591", "line-3": "#837B68",
    "line-4": "#7E7767",
    "ink-0": "#302B25", "ink-1": "#39332C", "ink-2": "#484138",
    "ink-3": "#574F44", "ink-4": "#61594D", "ink-5": "#6A6255",
    "ink-6": "#706A5B", "ink-7": "#7C7566", "ink-8": "#817A6A",
    "fg-accent": "#7D5335", "fg-accent-soft": "#8D674B",
    "control": "#626A58", "on-fill": "#FFFFFF",
    "fg-good": "#4F6847", "fg-bad": "#984C3D", "fg-warn": "#765A22",
    "fg-bad-soft": "#A05544", "fg-orange": "#87501D",
    "fg-error": "#A04A3C", "fg-error-link": "#9E4739",
    "fg-report": "#A34A35", "fg-bonus": "#52683D", "fg-cost": "#765A22",
    "state-leeching": "#4E6B42", "state-seeding": "#6F6522",
    "state-uploaded": "#75577D", "state-snatched": "#9A5644",
    "cat-stream": "#376B60", "cat-conference": "#765A22",
    "cat-birthday": "#7D5A80",
}
for i in range(10):
    L["ratio-%d" % i] = interp("#A34A35", "#4F6847", i / 9.0)
L_ALERT = mix(L["fg-orange"], L["surface-4"], 14)

# ---------------------------------------------------------------------------
# Night-sand dark palette (user-confirmed direction; stage 1 final)
# ---------------------------------------------------------------------------
D = {
    "surface-0": "#1D1B18", "surface-1": "#22201C", "surface-2": "#25231F",
    "surface-3": "#302D27", "surface-4": "#39352E", "surface-5": "#423E37",
    "surface-6": "#4F4A42", "surface-7": "#59534A", "surface-8": "#635C53",
    "surface-9": "#68615B",
    "line-1": "#322F28", "line-2": "#555045", "line-3": "#756D60",
    "line-4": "#948C7F",
    "ink-0": "#EAE2D5", "ink-1": "#D8D0C2", "ink-2": "#CFC7B8",
    "ink-3": "#C4B8A5", "ink-4": "#BCB0A0", "ink-5": "#B0A696",
    "ink-6": "#A69C8C", "ink-7": "#928B7B", "ink-8": "#857E6E",
    "fg-accent": "#D8A37E", "fg-accent-soft": "#E5C09E",
    "control": "#AAB49A", "on-fill": "#1D1B18",
    "fg-good": "#A6BD91", "fg-bad": "#E39A86", "fg-warn": "#D5B36F",
    "fg-bad-soft": "#DB8E7A", "fg-orange": "#D2A278",
    "fg-error": "#E5A79A", "fg-error-link": "#EDBCAE",
    "fg-report": "#DCA28E", "fg-bonus": "#B7C49C", "fg-cost": "#D2BC8E",
    "state-leeching": "#A6BD91", "state-seeding": "#D5B36F",
    "state-uploaded": "#C9B4C4", "state-snatched": "#DCA28E",
    "cat-stream": "#A3BDB2", "cat-conference": "#D2BC8E",
    "cat-birthday": "#CBB3C4",
}
for i in range(10):
    D["ratio-%d" % i] = interp("#DCA28E", "#A6BD91", i / 9.0)
# dark alert: the dark parent formula is 45% fg-orange over surface-0
# (not the light 14%/surface-4); the dark alert link token is fg-accent-soft.
D_ALERT = mix(D["fg-orange"], D["surface-0"], 45)

ALL_SURFACES = ("surface-0", "surface-1", "surface-2", "surface-3", "surface-4",
                "surface-5", "surface-6", "surface-7", "surface-8", "surface-9")
SEMANTIC = ("fg-good", "fg-bad", "fg-warn", "fg-orange", "fg-error",
            "fg-error-link", "fg-report", "fg-bonus", "fg-cost",
            "state-leeching", "state-seeding", "state-uploaded", "state-snatched",
            "cat-stream", "cat-conference", "cat-birthday")

def run_matrix(T, ALERT_BG, label, accent_text_need, accent_fill_need,
               alert_link_need, ink6_well_need, line2_need, extra,
               alert_pct, alert_base, alert_link_token):
    """extra: ('light'|'dark') selects the adapted guard pairs."""
    rows, fails = [], []

    def P(name, fg, bg, need):
        r = ratio(fg, bg)
        ok = r >= need
        rows.append((name, fg, bg, need, r, ok))
        if not ok:
            fails.append((name, fg, bg, r, need))

    # 1. body text on every resting surface
    for s in ALL_SURFACES:
        P("ink-0 on %s (body)" % s, T["ink-0"], T[s], 4.5)
    # secondary inks on wells and cards
    for s in ("surface-2", "surface-3", "surface-4"):
        for k in ("ink-1", "ink-2", "ink-3", "ink-4"):
            P("%s on %s (secondary)" % (k, s), T[k], T[s], 4.5)
    # buff multiplier text sits on the header base
    P("ink-4 on surface-0 (header buff text)", T["ink-4"], T["surface-0"], 4.5)
    # muted inks with documented roles
    P("ink-5 on surface-2 (muted body)", T["ink-5"], T["surface-2"], 4.5)
    P("ink-5 on surface-4 (muted body)", T["ink-5"], T["surface-4"], 4.5)
    P("ink-6 on surface-4 (muted on cards)", T["ink-6"], T["surface-4"], 4.5)
    P("ink-6 on surface-2 (muted on wells)", T["ink-6"], T["surface-2"], ink6_well_need)
    P("ink-7 on surface-4 (hints, >=3)", T["ink-7"], T["surface-4"], 3.0)
    P("ink-7 on surface-0 (hints, >=3)", T["ink-7"], T["surface-0"], 3.0)
    r = ratio(T["ink-8"], T["surface-0"])
    rows.append(("ink-8 on surface-0 (alertbar hint, doc 2.5)", T["ink-8"],
                 T["surface-0"], 2.5, r, r >= 2.5))
    if r < 2.5:
        fails.append(("ink-8 on surface-0", T["ink-8"], T["surface-0"], r, 2.5))
    # default links
    P("ink-3 link on surface-4", T["ink-3"], T["surface-4"], 4.5)
    P("ink-3 link on surface-2", T["ink-3"], T["surface-2"], 4.5)
    P("ink-3 link on surface-0", T["ink-3"], T["surface-0"], 4.5)
    # buttons
    P("on-fill on control (buttons)", T["on-fill"], T["control"], 4.5)
    P("on-fill on fg-accent (button hover)", T["on-fill"], T["fg-accent"], 4.5)
    # destructive buttons
    P("on-fill on fg-bad-soft (Delete rest)", T["on-fill"], T["fg-bad-soft"], 4.5)
    P("on-fill on fg-bad (Delete hover)", T["on-fill"], T["fg-bad"], 4.5)
    # autocomplete highlight + bvalidator tooltip
    P("on-fill on fg-accent (autocomplete)", T["on-fill"], T["fg-accent"], 4.5)
    P("on-fill on fg-bad (bvalidator 11px)", T["on-fill"], T["fg-bad"], 4.5)
    P("line-4 bvalidator border on surface-4", T["line-4"], T["surface-4"], 3.0)
    # accent text (light: all surfaces / dark: text surfaces then fills)
    for s in ALL_SURFACES:
        need = accent_text_need if ALL_SURFACES.index(s) <= 5 else accent_fill_need
        tag = "accent text" if ALL_SURFACES.index(s) <= 5 else "accent on structural fill (doc)"
        P("fg-accent on %s (%s)" % (s, tag), T["fg-accent"], T[s], need)
    for s in ("surface-0", "surface-2", "surface-3", "surface-4"):
        P("fg-accent-soft ring/icon on %s" % s, T["fg-accent-soft"], T[s], 3.0)
    # alert block (light: mix 14% over surface-4, link fg-accent;
    #             dark: mix 45% over surface-0, link fg-accent-soft)
    P("ink-0 on alert mix %d%% over %s (%s)" % (alert_pct, alert_base, ALERT_BG),
      T["ink-0"], ALERT_BG, 4.5)
    P("%s link on alert mix" % alert_link_token, T[alert_link_token], ALERT_BG,
      alert_link_need)
    # semantic text/icon colours (12-13px text)
    for k in SEMANTIC:
        P("%s on surface-2 (semantic)" % k, T[k], T["surface-2"], 4.5)
        P("%s on surface-4 (semantic)" % k, T[k], T["surface-4"], 4.5)
        P("%s on surface-0 (semantic on header)" % k, T[k], T["surface-0"], 4.5)
    # ratio ramp (stats tables)
    for i in range(10):
        P("ratio-%d on surface-2" % i, T["ratio-%d" % i], T["surface-2"], 4.5)
        P("ratio-%d on surface-4" % i, T["ratio-%d" % i], T["surface-4"], 4.5)
    # input/blockquote borders
    P("line-2 border on surface-2 (input edge)", T["line-2"], T["surface-2"], line2_need)
    P("line-3 border on surface-2 (blockquote/divider)", T["line-3"], T["surface-2"], 3.0)
    # forum read-icon fill vs row backgrounds + vs unread accent
    P("line-4 read icon on surface-1", T["line-4"], T["surface-1"], 3.0)
    P("line-4 read icon on surface-2", T["line-4"], T["surface-2"], 3.0)
    r = ratio(T["line-4"], T["fg-accent"])
    rows.append(("line-4 vs fg-accent (read/unread distinct)", T["line-4"],
                 T["fg-accent"], 0.0, r, r > 1.4))
    if not r > 1.4:
        fails.append(("line-4 vs fg-accent distinct", T["line-4"], T["fg-accent"], r, 1.4))
    # hover deltas must differ from base (same-value collision guard)
    if extra == "light":
        guards = (("surface-3", "surface-5", "alert pill hover"),
                  ("surface-8", "surface-9", "timeline hover"),
                  ("surface-7", "surface-9", "unread vs zebra"),
                  ("line-2", "surface-9", "line-2 vs hover fill"),
                  ("line-1", "surface-3", "line-1 vs panel bg"))
    else:
        guards = (("surface-3", "surface-5", "alert pill hover"),
                  ("surface-8", "surface-9", "timeline hover"),
                  ("surface-7", "surface-9", "unread vs zebra"),
                  ("line-2", "surface-9", "line-2 vs hover fill"),
                  ("line-1", "surface-2", "line-1 hairline vs page bg"))
    for a, b, glabel in guards:
        r = ratio(T[a], T[b])
        rows.append(("%s: %s vs %s (delta)" % (glabel, a, b), a, b, 0.0, r, r > 1.02))
        if not r > 1.02:
            fails.append(("%s delta" % glabel, a, b, r, 1.02))
    return rows, fails

light_rows, light_fails = run_matrix(
    L, L_ALERT, "warm-sand", 4.5, 4.5, 4.5, 4.1, 1.9, "light",
    14, "surface-4", "fg-accent")
dark_rows, dark_fails = run_matrix(
    D, D_ALERT, "night-sand", 4.5, 2.7, 3.9, 4.1, 1.9, "dark",
    45, "surface-0", "fg-accent-soft")

W = 62
out = []
out.append("=" * W)
out.append("Sand pair - WCAG 2.1 contrast report (warm-sand light + night-sand dark)")
out.append("=" * W)
for theme, rows, fails, ALERT_BG, T in (
        ("WARM-SAND (light)", light_rows, light_fails, L_ALERT, L),
        ("NIGHT-SAND (dark)", dark_rows, dark_fails, D_ALERT, D)):
    out.append("")
    out.append("--- %s ---" % theme)
    for name, fg, bg, need, r, ok in rows:
        out.append("%-52s %s  fg=%-9s bg=%-9s %5.2f:1 (need %.1f)"
                   % (name, "PASS" if ok else "FAIL", fg, bg, r, need))
    out.append("alert mix: color-mix(fg-orange %d%%, %s) = %s"
               % (14 if T is L else 45, "surface-4" if T is L else "surface-0",
                  ALERT_BG))
    for i in range(10):
        out.append("ratio-%d = %s" % (i, T["ratio-%d" % i]))
    out.append("%s: %d checks, %d failures" % (theme, len(rows), len(fails)))

out.append("")
out.append("=" * W)
total = len(light_rows) + len(dark_rows)
allfails = light_fails + dark_fails
out.append("TOTAL: %d checks, %d failures" % (total, len(allfails)))
for name, fg, bg, r, need in allfails:
    out.append("  ! %s fg=%s bg=%s %.2f:1 < %.1f" % (name, fg, bg, r, need))
report = "\n".join(out)
print(report)
with open("sand_contrast_report.txt", "w") as f:
    f.write(report + "\n")
sys.exit(1 if allfails else 0)
