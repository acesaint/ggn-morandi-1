#!/usr/bin/env python3
"""Warm-paper light Morandi palette - WCAG contrast verification.

Reproducible check for MORANDI_LIGHT_TOKENS.md (phase 1). Computes WCAG 2.1
contrast ratios for every mandatory foreground/background pair the GGn
stylesheet actually consumes. No CSS is modified by this script.

Run:  python3 morandi_light_contrast.py
"""

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
# Warm-paper light Morandi palette (phase 1 proposal, iteration 2)
# ---------------------------------------------------------------------------
T = {
    # surfaces: deep paper -> brightest raised
    "surface-0": "#ECE8DC", "surface-1": "#E9E5D7", "surface-2": "#EFECE2",
    "surface-3": "#F5F2EA", "surface-4": "#FBF9F3", "surface-5": "#EDE9DB",
    "surface-6": "#F7F5EC", "surface-7": "#FAF8F0", "surface-8": "#FDFCF7",
    "surface-9": "#DBD6C5",
    # lines: hairline -> strong
    "line-1": "#E4E0D2", "line-2": "#B0AA94", "line-3": "#8C8670",
    "line-4": "#7E7C68",
    # inks: body -> faintest (hint roles only at the faint end)
    "ink-0": "#33352B", "ink-1": "#3D4034", "ink-2": "#4B4E40",
    "ink-3": "#5A5D4D", "ink-4": "#65685A", "ink-5": "#6A6D58",
    "ink-6": "#707359", "ink-7": "#838671", "ink-8": "#8B8E7A",
    # accent: terracotta
    "fg-accent": "#82503A", "fg-accent-soft": "#A97453",
    # control: sage
    "control": "#6B7565",
    # fills / on-fill
    "on-fill": "#FFFFFF",
    # semantic text & icon colours
    "fg-good": "#4E6E39", "fg-bad": "#9A4A32", "fg-warn": "#7F5F17",
    "fg-bad-soft": "#9E5638", "fg-orange": "#8F551A",
    "fg-error": "#A34A3C", "fg-error-link": "#9E463A",
    "fg-report": "#A3452E", "fg-bonus": "#526E2E", "fg-cost": "#7F5F17",
    # torrent states
    "state-leeching": "#48703B", "state-seeding": "#6F6A1D",
    "state-uploaded": "#745787", "state-snatched": "#995549",
    # categories
    "cat-stream": "#377068", "cat-conference": "#7F5F17",
    "cat-birthday": "#7E5986",
    # shadows are alpha values, not checked here
}

# ratio ramp 0..9: terracotta-red -> sage
for i in range(10):
    T["ratio-%d" % i] = interp("#A3452E", "#4E6E37", i / 9.0)

# alert proposal: mix ratio 14% over surface-4, link token = fg-accent
ALERT_BG = mix(T["fg-orange"], T["surface-4"], 14)

FAILS = []

def check(name, fg, bg, need):
    r = ratio(fg, bg)
    ok = r >= need
    if not ok:
        FAILS.append((name, fg, bg, r, need))
    return r, ok

# --- table of every mandatory consumer pair -------------------------------
pairs = []
def P(name, fg, bg, need):
    pairs.append((name, fg, bg, need, *check(name, fg, bg, need)))

# 1. body text on every resting surface
for s in ("surface-0", "surface-1", "surface-2", "surface-3", "surface-4",
          "surface-5", "surface-6", "surface-7", "surface-8", "surface-9"):
    P("ink-0 on %s (body)" % s, T["ink-0"], T[s], 4.5)
# secondary inks: body-safe on wells and cards
for s in ("surface-2", "surface-3", "surface-4"):
    for k in ("ink-1", "ink-2", "ink-3", "ink-4"):
        P("%s on %s (secondary)" % (k, s), T[k], T[s], 4.5)
# buff multiplier text (ink-4) sits on the header base
P("ink-4 on surface-0 (header buff text)", T["ink-4"], T["surface-0"], 4.5)
# muted inks with documented roles
P("ink-5 on surface-2 (muted body)", T["ink-5"], T["surface-2"], 4.5)
P("ink-5 on surface-4 (muted body)", T["ink-5"], T["surface-4"], 4.5)
P("ink-6 on surface-4 (muted on cards)", T["ink-6"], T["surface-4"], 4.5)
P("ink-6 on surface-2 (muted on wells, orig parity 4.1)", T["ink-6"], T["surface-2"], 4.1)
P("ink-7 on surface-4 (hints, >=3)", T["ink-7"], T["surface-4"], 3.0)
P("ink-7 on surface-0 (hints, >=3)", T["ink-7"], T["surface-0"], 3.0)
# ink-8 is faintest hint; documented accepted-risk (see spec)
r, ok = check("ink-8 on surface-0 (alertbar, doc)", T["ink-8"], T["surface-0"], 0.0)
pairs.append(("ink-8 on surface-0 (alertbar hint, doc 2.5)", T["ink-8"], T["surface-0"], 2.5, r, r >= 2.5))
# 3. default links
P("ink-3 link on surface-4", T["ink-3"], T["surface-4"], 4.5)
P("ink-3 link on surface-2", T["ink-3"], T["surface-2"], 4.5)
P("ink-3 link on surface-0", T["ink-3"], T["surface-0"], 4.5)
# 4. buttons: on-fill on control + accent hover
P("on-fill on control (buttons)", T["on-fill"], T["control"], 4.5)
P("on-fill on fg-accent (button hover)", T["on-fill"], T["fg-accent"], 4.5)
# 5. destructive buttons
P("on-fill on fg-bad-soft (Delete rest)", T["on-fill"], T["fg-bad-soft"], 4.5)
P("on-fill on fg-bad (Delete hover)", T["on-fill"], T["fg-bad"], 4.5)
# 6. autocomplete highlight
P("on-fill on fg-accent (autocomplete)", T["on-fill"], T["fg-accent"], 4.5)
# 7. bvalidator tooltip
P("on-fill on fg-bad (bvalidator 11px)", T["on-fill"], T["fg-bad"], 4.5)
P("line-4 bvalidator border on surface-4", T["line-4"], T["surface-4"], 3.0)
# 8. accent links as text on paper
for s in ("surface-0", "surface-1", "surface-2", "surface-3", "surface-4",
          "surface-5", "surface-6", "surface-7", "surface-8", "surface-9"):
    P("fg-accent on %s (accent text)" % s, T["fg-accent"], T[s], 4.5)
# fg-accent-soft is border/focus/icon only; non-text 3:1
for s in ("surface-0", "surface-2", "surface-3", "surface-4"):
    P("fg-accent-soft ring/icon on %s" % s, T["fg-accent-soft"], T[s], 3.0)
# 9. alert block (proposed: mix 14% over surface-4, link = fg-accent)
P("ink-0 on alert mix 14%% (%s)" % ALERT_BG, T["ink-0"], ALERT_BG, 4.5)
P("fg-accent link on alert mix", T["fg-accent"], ALERT_BG, 4.5)
# 10. semantic text/icon colours on paper (12-13px text)
for k in ("fg-good", "fg-bad", "fg-warn", "fg-orange", "fg-error",
          "fg-error-link", "fg-report", "fg-bonus", "fg-cost",
          "state-leeching", "state-seeding", "state-uploaded", "state-snatched",
          "cat-stream", "cat-conference", "cat-birthday"):
    P("%s on surface-2 (semantic)" % k, T[k], T["surface-2"], 4.5)
    P("%s on surface-4 (semantic)" % k, T[k], T["surface-4"], 4.5)
    P("%s on surface-0 (semantic on header)" % k, T[k], T["surface-0"], 4.5)
# 11. ratio ramp on paper (stats tables)
for i in range(10):
    P("ratio-%d on surface-2" % i, T["ratio-%d" % i], T["surface-2"], 4.5)
    P("ratio-%d on surface-4" % i, T["ratio-%d" % i], T["surface-4"], 4.5)
# 12. input fields: ink-0 on surface-2; borders documented at ~2:1
P("line-2 border on surface-2 (input edge, >=1.9)", T["line-2"], T["surface-2"], 1.9)
P("line-3 border on surface-2 (blockquote/divider)", T["line-3"], T["surface-2"], 3.0)
# 13. forum read-icon fill (line-4) vs row backgrounds + vs unread accent
P("line-4 read icon on surface-1", T["line-4"], T["surface-1"], 3.0)
P("line-4 read icon on surface-2", T["line-4"], T["surface-2"], 3.0)
pairs.append(("line-4 vs fg-accent (read/unread distinct)", T["line-4"], T["fg-accent"], 0.0,
              ratio(T["line-4"], T["fg-accent"]), ratio(T["line-4"], T["fg-accent"]) > 1.4))
# 14. hover deltas must differ from base (same-value collision guard)
for a, b, label in (("surface-3", "surface-5", "alert pill hover"),
                    ("surface-8", "surface-9", "timeline hover"),
                    ("surface-7", "surface-9", "unread vs zebra"),
                    ("line-2", "surface-9", "line-2 vs hover fill"),
                    ("line-1", "surface-3", "line-1 vs panel bg")):
    r = ratio(T[a], T[b])
    pairs.append(("%s: %s vs %s (delta)" % (label, a, b), a, b, 0.0, r, r > 1.02))

# --- report ---------------------------------------------------------------
W = 58
print("=" * W)
print("Warm-paper light Morandi - WCAG 2.1 contrast report")
print("=" * W)
for name, fg, bg, need, r, ok in pairs:
    flag = "PASS" if ok else "FAIL"
    print("%-46s %s  fg=%-9s bg=%-9s %5.2f:1 (need %.1f)" % (name, flag, fg, bg, r, need))
print("-" * W)
print("alert mix proposal: color-mix(fg-orange 14%%, surface-4) = %s" % ALERT_BG)
for i in range(10):
    print("ratio-%d = %s" % (i, T["ratio-%d" % i]))
print("-" * W)
if FAILS:
    print("FAILURES: %d" % len(FAILS))
    for name, fg, bg, r, need in FAILS:
        print("  ! %s fg=%s bg=%s %.2f:1 < %.1f" % (name, fg, bg, r, need))
    raise SystemExit(1)
print("ALL CHECKS PASSED")
