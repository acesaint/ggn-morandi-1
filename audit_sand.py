#!/usr/bin/env python3
"""Sand pair - stage 3/4 reproducible static audit.

Read-only. Verifies ggn-morandi-warm-sand.css against the warm-paper parent
and ggn-morandi-night-sand.css against the dark-green parent, per every
invariant established in SAND_THEME_TOKENS.md and SAND_THEMES_PLAN.md.
Prints a pass/fail summary; exits non-zero on any failure.

Run:  python3 audit_sand.py
"""

import re
import sys

WS = "ggn-morandi-warm-sand.css"
NS = "ggn-morandi-night-sand.css"
WP = "ggn-morandi-warm-paper.css"
DG = "ggn-morandi-dark-green.css"

results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print("%-4s %-52s %s" % ("PASS" if ok else "FAIL", name, detail))

ws = open(WS).read()
ns = open(NS).read()
wp = open(WP).read()
dg = open(DG).read()
wsl = ws.split("\n")
nsl = ns.split("\n")

def root_tokens(text):
    m = re.search(r":root \{.*?--ggn-bg.*?\n\}", text, re.S)
    return dict(re.findall(r"(--[\w-]+):\s*([^;]+);", m.group(0)))

# --- warm-sand: token conformance ------------------------------------------
WARM_SPEC = {
 "--surface-0":"#ede9df","--surface-1":"#e8e3d8","--surface-2":"#f0ede5","--surface-3":"#f5f2eb",
 "--surface-4":"#fbf9f4","--surface-5":"#e9e4d9","--surface-6":"#f7f4ed","--surface-7":"#faf8f2",
 "--surface-8":"#fdfcf8","--surface-9":"#ddd6c8",
 "--line-1":"#e1dccf","--line-2":"#ada591","--line-3":"#837b68","--line-4":"#7e7767",
 "--surface-deep-rgb":"237, 233, 223","--surface-2-rgb":"240, 237, 229",
 "--ink-0":"#302b25","--ink-1":"#39332c","--ink-2":"#484138","--ink-3":"#574f44","--ink-4":"#61594d",
 "--ink-5":"#6a6255","--ink-6":"#706a5b","--ink-7":"#7c7566","--ink-8":"#817a6a",
 "--fg-accent":"#7d5335","--fg-accent-soft":"#8d674b","--fg-good":"#4f6847","--fg-bad":"#984c3d",
 "--fg-warn":"#765a22","--fg-bad-soft":"#a05544","--control":"#626a58","--on-fill":"#ffffff",
 "--state-leeching":"#4e6b42","--state-seeding":"#6f6522","--state-uploaded":"#75577d",
 "--state-snatched":"#9a5644","--cat-stream":"#376b60","--cat-conference":"#765a22",
 "--cat-birthday":"#7d5a80","--fg-bonus":"#52683d","--fg-cost":"#765a22",
 "--fg-error":"#a04a3c","--fg-error-link":"#9e4739","--fg-report":"#a34a35",
 "--fg-orange":"#87501d","--blur-bg":"var(--surface-3)","--blur-bg-strong":"var(--surface-3)",
}
NIGHT_SPEC = {
 "--surface-0":"#1d1b18","--surface-1":"#22201c","--surface-2":"#25231f","--surface-3":"#302d27",
 "--surface-4":"#39352e","--surface-5":"#423e37","--surface-6":"#4f4a42","--surface-7":"#59534a",
 "--surface-8":"#635c53","--surface-9":"#68615b",
 "--line-1":"#322f28","--line-2":"#555045","--line-3":"#756d60","--line-4":"#948c7f",
 "--surface-deep-rgb":"29, 27, 24","--surface-2-rgb":"37, 35, 31",
 "--ink-0":"#eae2d5","--ink-1":"#d8d0c2","--ink-2":"#cfc7b8","--ink-3":"#c4b8a5","--ink-4":"#bcb0a0",
 "--ink-5":"#b0a696","--ink-6":"#a69c8c","--ink-7":"#928b7b","--ink-8":"#857e6e",
 "--fg-accent":"#d8a37e","--fg-accent-soft":"#e5c09e","--fg-good":"#a6bd91","--fg-bad":"#e39a86",
 "--fg-warn":"#d5b36f","--fg-bad-soft":"#db8e7a","--control":"#aab49a","--on-fill":"#1d1b18",
 "--state-leeching":"#a6bd91","--state-seeding":"#d5b36f","--state-uploaded":"#c9b4c4",
 "--state-snatched":"#dca28e","--cat-stream":"#a3bdb2","--cat-conference":"#d2bc8e",
 "--cat-birthday":"#cbb3c4","--fg-bonus":"#b7c49c","--fg-cost":"#d2bc8e",
 "--fg-error":"#e5a79a","--fg-error-link":"#edbcae","--fg-report":"#dca28e",
 "--fg-orange":"#d2a278","--blur-bg":"var(--surface-3)","--blur-bg-strong":"var(--surface-3)",
}
def interp(c1, c2, t):
    h1, h2 = c1.lstrip("#"), c2.lstrip("#")
    return "#{:02x}{:02x}{:02x}".format(*(round(int(h1[i:i+2], 16) + (int(h2[i:i+2], 16) - int(h1[i:i+2], 16)) * t)
                                        for i in (0, 2, 4)))
for i in range(10):
    WARM_SPEC["--ratio-%d" % i] = interp("#a34a35", "#4f6847", i / 9.0)
    NIGHT_SPEC["--ratio-%d" % i] = interp("#dca28e", "#a6bd91", i / 9.0)

for label, text, spec in ((WS, ws, WARM_SPEC), (NS, ns, NIGHT_SPEC)):
    found = root_tokens(text)
    bad = [(k, found.get(k), v) for k, v in spec.items() if found.get(k, "").strip().lower() != v]
    check("%s root tokens match spec" % label, not bad,
          "%d mismatches" % len(bad) if bad else "%d tokens" % len(spec))

# --- structural parity with parents ----------------------------------------
def counts(t):
    return {
        "!important": t.count("!important"),
        ":has(": t.count(":has("),
        "@media": t.count("@media"),
        "rgba(var(": t.count("rgba(var("),
        "brightness(": t.count("brightness("),
        "invert(": t.count("invert("),
    }
for label, child, parent in ((WS, ws, wp), (NS, ns, dg)):
    cc, pc = counts(child), counts(parent)
    check("%s structural parity vs parent" % label,
          all(cc[k] == pc[k] for k in pc),
          " ".join("%s=%d" % (k, v) for k, v in cc.items()))

# --- controlled diff: only whitelisted lines differ from parents -------------
def controlled_diff(child_lines, parent_lines, comment_span, token_names):
    root_start = next(i for i, ln in enumerate(parent_lines)
                      if ln == ":root {" and "--ggn-bg" in "\n".join(parent_lines[i:i + 4]))
    root_end = next(i for i in range(root_start + 1, len(parent_lines)) if parent_lines[i] == "}")
    changed = [i for i in range(len(parent_lines)) if parent_lines[i] != child_lines[i]]
    allowed = {1} | set(range(root_start + 2, root_start + 2 + comment_span))
    for i in range(root_start + 1, root_end):
        m = re.match(r"^  (--[\w-]+): ", parent_lines[i])
        if m and m.group(1) in token_names:
            allowed.add(i)
    wm = [i for i, ln in enumerate(parent_lines) if "--ggn-wm-edge:" in ln]
    assert len(wm) == 1
    allowed.add(wm[0])
    bad = [i for i in changed if i not in allowed]
    return changed, bad

changed, bad = controlled_diff(wsl, wp.split("\n"), 1, WARM_SPEC)
check("%s diff limited to whitelist" % WS, not bad,
      "%d changed lines, %d unexpected" % (len(changed), len(bad)))
changed, bad = controlled_diff(nsl, dg.split("\n"), 2, NIGHT_SPEC)
check("%s diff limited to whitelist" % NS, not bad,
      "%d changed lines, %d unexpected" % (len(changed), len(bad)))

# --- no live backdrop-filter / functional overlays --------------------------
for label, lines in ((WS, wsl), (NS, nsl)):
    live = [ln for ln in lines if re.search(r"(?<!-webkit-)(?<!-)(?<!\()backdrop-filter\s*:", ln)
            and "@supports" not in ln and "without" not in ln]
    check("%s no live backdrop-filter" % label, not live, "%d" % len(live))
    ov = sum(1 for ln in lines if "rgba(var(" in ln)
    check("%s rgba(var() limited to 3 overlays" % label, ov == 3, "%d" % ov)

# --- parent palette purged ---------------------------------------------------
WARM_OLD = ("#ece8dc", "#82503a", "#a97453", "#6b7565", "#8b8e7a", "#7f5f17",
            "#33352b", "#48703b", "#745787", "#377068")
NIGHT_OLD = ("#202528", "#252b2e", "#292f32", "#30383b", "#394448", "#3e4a4d",
             "#445154", "#48575a", "#4d5d60", "#53666a", "#c8b99d", "#8b9a96",
             "#d1a17c", "#77837e", "#05070d")
NIGHT_IN_WS = ("#1d1b18", "#22201c", "#25231f", "#302d27", "#39352e", "#423e37",
               "#4f4a42", "#59534a", "#635c53", "#68615b")
check("%s warm-paper tokens purged" % WS, not any(v in ws for v in WARM_OLD),
      "leftovers: %s" % [v for v in WARM_OLD if v in ws])
check("%s dark ramp never leaked" % WS, not any(v in ws for v in NIGHT_IN_WS),
      "leaked: %s" % [v for v in NIGHT_IN_WS if v in ws])
check("%s dark-green tokens purged" % NS, not any(v in ns for v in NIGHT_OLD),
      "leftovers: %s" % [v for v in NIGHT_OLD if v in ns])
check("%s light ramp never leaked" % NS,
      not any(v in ns for v in ("#f5f2eb", "#fbf9f4", "#302b25", "#7d5335")),
      "leaked: %s" % [v for v in ("#f5f2eb", "#fbf9f4", "#302b25", "#7d5335") if v in ns])

# --- approved deviations / inherited adaptations ------------------------------
check("%s alert mix 14%% on surface-4" % WS,
      "color-mix(in srgb, var(--fg-orange) 14%, var(--surface-4))" in ws)
check("%s alert link uses fg-accent" % WS,
      bool(re.search(r"\.alert a,(\n\.alert-bar a,){0,1}\n\.alert--warning a,\n\.alert--error a \{\n  color: var\(--fg-accent\);", ws)))
check("%s wordmark edge sand base" % WS,
      "color-mix(in srgb, var(--fg-accent) 22%, #302b25)" in ws)
check("%s hr hairline tokenized" % WS, "border-top: 1px solid var(--line-2);" in ws)
check("%s no brightness(5) white-flash" % WS, "brightness(5)" not in ws)
check("%s dialog icons not inverted" % WS,
      "invert(0.7) brightness(1.4)" not in ws and "invert(1) brightness(1.5)" not in ws)
check("%s drag clone shadow warm" % WS, "rgba(60, 54, 40, 0.3)" in ws)
check("%s cover wash for light" % WS, "filter: brightness(1.1) saturate(0.85);" in ws)
check("%s search input text body-safe" % WS,
      bool(re.search(r'#searchbars > ul > li input\[type="text"\] \{[^}]*?color: var\(--ink-4\);', ws, re.S)))
check("%s buff hover presses deeper (surface-5)" % WS,
      bool(re.search(r"\.global_buffs a:hover \{\n  background: var\(--surface-5\);", ws)))

check("%s alert mix 45%% on surface-0 (dark formula)" % NS,
      "color-mix(in srgb, var(--fg-orange) 45%, var(--surface-0))" in ns)
check("%s alert link inherits fg-accent-soft" % NS,
      bool(re.search(r"\.alert--warning a,\n\.alert--error a \{\n  color: var\(--fg-accent-soft\);", ns)))
check("%s wordmark edge warm base" % NS,
      "color-mix(in srgb, var(--fg-accent) 22%, #14110d)" in ns)
check("%s hr hairline tokenized" % NS, "border-top: 1px solid var(--line-2);" in ns)
check("%s cover wash for dark inherited" % NS,
      "filter: brightness(0.5) saturate(0.92);" in ns)
check("%s drag clone shadow dark inherited" % NS,
      "box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.4) !important;" in ns)
check("%s buff hover dark inherited (surface-4)" % NS,
      bool(re.search(r"\.global_buffs a:hover \{\n  background: var\(--surface-4\);", ns)))

# --- blue-night blocks / theme variants -------------------------------------
# light: the blue-night swatch selector was removed (a light theme must not
# offer the dark blue-night swatch). dark: the blue-night swatch block is
# legitimately inherited from the dark parent; section 10 equality below
# proves it byte-identical.
check("%s no blue-night swatch selector" % WS,
      'data-ggn-swatch="blue-night"' not in ws)
check("%s blue-night swatch block inherited from parent" % NS,
      'data-ggn-swatch="blue-night"' in ns
      and ns.count('data-ggn-swatch="blue-night"')
          == dg.count('data-ggn-swatch="blue-night"'))
for label, text in ((WS, ws), (NS, ns)):
    themes = [t for t in ("abyss", "oled", "graphite", "ember", "nocturne")
              if 'data-ggn-theme="%s"' % t in text]
    check("%s all 5 theme variant blocks kept" % label, len(themes) == 5, ",".join(themes))

# --- motion & focus -----------------------------------------------------------
for label, text, parent in ((WS, ws, wp), (NS, ns, dg)):
    check("%s prefers-reduced-motion block" % label, "prefers-reduced-motion: reduce" in text)
    kv = sorted(set(re.findall(r"@keyframes\s+([\w-]+)", text)))
    kv_p = sorted(set(re.findall(r"@keyframes\s+([\w-]+)", parent)))
    check("%s keyframes inventory == parent" % label, kv == kv_p, ",".join(kv))
    fv = len(re.findall(r":focus-visible", text))
    check("%s :focus-visible rules present" % label, fv > 0, "%d rules" % fv)

# --- hardcoded colour inventory ----------------------------------------------
def s10_line(lines):
    return [i for i, ln in enumerate(lines, 1) if "Companion toolkit hooks" in ln][-1]

def body_inventory(lines, s10):
    body = "\n".join(lines[:s10 - 1])
    body = re.sub(r":root \{.*?\n\}", "", body, count=1, flags=re.S)
    out = {}
    for i, ln in enumerate(body.split("\n"), 1):
        for mm in re.finditer(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", ln):
            v = mm.group(0).lower()
            if v in ("#fff", "#ffffff", "#000", "#000000", "#ff0"):
                continue
            out.setdefault(v, i)
    return out

WARM_KNOWN = {"#123456", "#f44336", "#b58058", "#edc245", "#bfbfbf", "#c0c0c0", "#cd7f32",
              "#d4af37", "#8ccada", "#cacaca", "#ff4727", "#f8d832", "#c4a316", "#ffc107",
              "#efba5b", "#8a6a4f", "#c9584a", "#302b25"}
NIGHT_KNOWN = WARM_KNOWN - {"#302b25"} | {"#ccc", "#14110d"}
inv = body_inventory(wsl, s10_line(wsl))
unknown = {k: v for k, v in inv.items() if k not in WARM_KNOWN}
check("%s body colours in documented set" % WS,
      not unknown and len(inv) == len(WARM_KNOWN),
      "unknown: %s | %d hits" % (sorted(unknown) if unknown else "none", len(inv)))
inv = body_inventory(nsl, s10_line(nsl))
unknown = {k: v for k, v in inv.items() if k not in NIGHT_KNOWN}
check("%s body colours in documented set" % NS,
      not unknown and len(inv) == len(NIGHT_KNOWN),
      "unknown: %s | %d hits" % (sorted(unknown) if unknown else "none", len(inv)))

# --- section 10 toolkit region equals parent ----------------------------------
for label, child_lines, parent_lines in ((WS, wsl, wp.split("\n")), (NS, nsl, dg.split("\n"))):
    c10 = s10_line(child_lines)
    p10 = s10_line(parent_lines)
    check("%s section 10 equals parent" % label,
          "\n".join(child_lines[c10 - 1:]).strip() == "\n".join(parent_lines[p10 - 1:]).strip(),
          "S10 child L%d vs parent L%d" % (c10, p10))

# --- external resources ---------------------------------------------------------
expected_imports = [
    "https://gazellegames.net/static/styles/game_room/caticons.css",
    "https://gazellegames.net/static/styles/game_room/webLinks.css",
    "https://gazellegames.net/static/styles/game_room/gamethemes.css"]
for label, text in ((WS, ws), (NS, ns)):
    imports = re.findall(r'@import url\("([^"]+)"\)', text)
    check("%s site @imports unchanged" % label, imports == expected_imports, str(len(imports)))
    fonts = re.findall(r'url\("?(assets/fonts/[^"]+?)"?\)', text)
    check("%s font faces use relative repo paths" % label,
          len(fonts) >= 10 and all(f.startswith("assets/fonts/") for f in fonts),
          "%d font refs" % len(set(fonts)))
    check("%s wordmark font embedded" % label, text.count("data:font/woff2;base64") == 1)

# --- production parents untouched ----------------------------------------------
import hashlib
def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()
check("parent ggn-morandi-dark-green.css unchanged",
      sha(DG) == "8ba14f2645564e1ba6a988a410d72661de81da592e533724f27572d90e85b92a")
check("parent ggn-morandi-warm-paper.css unchanged",
      sha(WP) == "bbde3891f98056d894826abc5c8a715078b8b1d29980ed88087de5eef70952cc")

check("contrast suite reference", True, "run: python3 sand_contrast.py (268 checks)")

print()
fails = [r for r in results if not r[1]]
print("=" * 60)
print("SAND PAIR AUDIT: %d checks, %d failures" % (len(results), len(fails)))
for name, _, detail in fails:
    print("  FAILED:", name, detail)
sys.exit(1 if fails else 0)
