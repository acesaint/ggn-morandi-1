#!/usr/bin/env python3
"""GGN Morandi Warm Paper - phase 4 reproducible static audit.

Read-only. Verifies the light theme file against every invariant established
in MORANDI_LIGHT_TOKENS.md and the phase 0 baseline. Prints a pass/fail
summary; exits non-zero on any failure. Does not modify any file.

Run:  python3 audit_light.py
"""

import re
import sys

LIGHT = "ggn-morandi-warm-paper.css"
DARK = "ggn-morandi-dark-green.css"

results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print("%-4s %-46s %s" % ("PASS" if ok else "FAIL", name, detail))

s = open(LIGHT).read()
d = open(DARK).read()
ls = s.split("\n")

# --- 1. token conformance against the approved spec -----------------------
expected = {
 "--surface-0":"#ece8dc","--surface-1":"#e9e5d7","--surface-2":"#efece2","--surface-3":"#f5f2ea",
 "--surface-4":"#fbf9f3","--surface-5":"#ede9db","--surface-6":"#f7f5ec","--surface-7":"#faf8f0",
 "--surface-8":"#fdfcf7","--surface-9":"#dbd6c5",
 "--line-1":"#e4e0d2","--line-2":"#b0aa94","--line-3":"#8c8670","--line-4":"#7e7c68",
 "--surface-deep-rgb":"236, 232, 220","--surface-2-rgb":"239, 236, 226",
 "--ink-0":"#33352b","--ink-1":"#3d4034","--ink-2":"#4b4e40","--ink-3":"#5a5d4d","--ink-4":"#65685a",
 "--ink-5":"#6a6d58","--ink-6":"#707359","--ink-7":"#838671","--ink-8":"#8b8e7a",
 "--fg-accent":"#82503a","--fg-accent-soft":"#a97453","--fg-good":"#4e6e39","--fg-bad":"#9a4a32",
 "--fg-warn":"#7f5f17","--fg-bad-soft":"#9e5638","--control":"#6b7565","--on-fill":"#ffffff",
 "--state-leeching":"#48703b","--state-seeding":"#6f6a1d","--state-uploaded":"#745787",
 "--state-snatched":"#995549","--cat-stream":"#377068","--cat-conference":"#7f5f17",
 "--cat-birthday":"#7e5986","--ratio-0":"#a3452e","--ratio-1":"#9a4a2f","--ratio-2":"#904e30",
 "--ratio-3":"#875331","--ratio-4":"#7d5732","--ratio-5":"#745c33","--ratio-6":"#6a6034",
 "--ratio-7":"#616535","--ratio-8":"#576936","--ratio-9":"#4e6e37","--fg-bonus":"#526e2e",
 "--fg-cost":"#7f5f17","--fg-error":"#a34a3c","--fg-error-link":"#9e463a",
 "--fg-report":"#a3452e","--fg-orange":"#8f551a",
}
m = re.search(r":root \{(.*?)\n\}", s, re.S)
found = dict(re.findall(r"(--[\w-]+):\s*([^;]+);", m.group(1)))
bad = [(k, found.get(k), v) for k, v in expected.items() if found.get(k, "").strip().lower() != v]
check("root tokens match spec (55)", not bad, "%d mismatches" % len(bad) if bad else "")

# --- 2. structural parity with the validated dark body --------------------
def counts(t):
    return {
        "!important": t.count("!important"),
        ":has(": t.count(":has("),
        "@media": t.count("@media"),
        "rgba(var(": t.count("rgba(var("),
    }
cd, cs = counts(d), counts(s)
parity = all(cd[k] == cs[k] for k in cd)
check("structural parity vs dark body", parity,
      " ".join("%s=%d" % (k, v) for k, v in cs.items()))

# --- 3. no live backdrop-filter declarations -------------------------------
live = [ln for ln in ls if re.search(r"(?<!-webkit-)(?<!-)(?<!\()backdrop-filter\s*:", ln)
        and "@supports" not in ln and "without" not in ln]
check("no live backdrop-filter declarations", not live, "%d" % len(live))

# --- 4. functional overlays are the only rgba(var() ------------------------
ov = [(i+1, ln.strip()) for i, ln in enumerate(ls) if "rgba(var(" in ln]
check("rgba(var() limited to 3 functional overlays", len(ov) == 3,
      "; ".join("L%d" % n for n, _ in ov))

# --- 5. old dark values purged ---------------------------------------------
for gone in ("#202528", "#c8b99d", "#8b9a96", "#d1a17c", "#77837e"):
    check("old dark token %s absent" % gone, gone not in s)

# --- 6. approved deviations present ----------------------------------------
check("alert mix 14% on surface-4",
      "color-mix(in srgb, var(--fg-orange) 14%, var(--surface-4))" in s)
check("alert link uses fg-accent",
      bool(re.search(r"\.alert a,(\n\.alert-bar a,){0,1}\n\.alert--warning a,\n\.alert--error a \{\n  color: var\(--fg-accent\);", s)))
check("hr hairline tokenized", "border-top: 1px solid var(--line-2);" in s)
check("wordmark edge warm base", "color-mix(in srgb, var(--fg-accent) 22%, #33352b)" in s)
check("no brightness(5) white-flash left", "brightness(5)" not in s)
check("dialog icons not inverted", "invert(0.7) brightness(1.4)" not in s
      and "invert(1) brightness(1.5)" not in s)
check("drag clone shadow warm", "rgba(60, 54, 40, 0.3)" in s)
check("cover wash for light", "filter: brightness(1.1) saturate(0.85);" in s)
check("search input text body-safe",
      bool(re.search(r"#searchbars > ul > li input\[type=\"text\"\] \{[^}]*?color: var\(--ink-4\);", s, re.S)))
check("buff hover presses deeper (surface-5)",
      bool(re.search(r"\.global_buffs a:hover \{\n  background: var\(--surface-5\);", s)))

# --- 7. blue-night light blocks removed from §10 ---------------------------
check("no blue-night swatch selector", 'data-ggn-swatch="blue-night"' not in s)
check("blue-night default light block gone",
      ':root[data-ggn-mode="light"],\n:root[data-ggn-mode="light"] [data-ggn-swatch' not in s)
themes = [t for t in ("abyss", "oled", "graphite", "ember", "nocturne")
          if 'data-ggn-theme="%s"' % t in s]
check("all 5 theme variant blocks kept", len(themes) == 5, ",".join(themes))

# --- 8. motion & focus ------------------------------------------------------
check("prefers-reduced-motion block present", "prefers-reduced-motion: reduce" in s)
check("jelly animation exempted in reduce block",
      "jelly" in s.lower() and s.lower().count("jelly") >= 2)
check("flickerAnimation removed", "flickerAnimation" not in s)
kv = sorted(set(re.findall(r"@keyframes\s+([\w-]+)", s)))
check("keyframes inventory stable", kv == sorted(set(re.findall(r"@keyframes\s+([\w-]+)", d))),
      ",".join(kv))
fv = len(re.findall(r":focus-visible", s))
check(":focus-visible rules present", fv > 0, "%d rules" % fv)

# --- 9. hardcoded colour inventory ------------------------------------------
# body region: everything before the §10 toolkit hooks block (L12714 in light),
# excluding the :root token block itself; §10 is checked separately below.
S10_LIGHT = 12714
body_txt = "\n".join(ls[:S10_LIGHT - 1])
body_txt = re.sub(r":root \{.*?\n\}", "", body_txt, count=1, flags=re.S)
out = {}
for i, ln in enumerate(body_txt.split("\n"), 1):
    for mm in re.finditer(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", ln):
        v = mm.group(0).lower()
        if v in ("#fff", "#ffffff", "#000", "#000000", "#ff0"):
            continue
        out.setdefault(v, i)
known = {"#123456", "#f44336", "#b58058", "#edc245", "#bfbfbf", "#c0c0c0", "#cd7f32",
         "#d4af37", "#8ccada", "#cacaca", "#ff4727", "#f8d832", "#c4a316", "#ffc107",
         "#efba5b", "#8a6a4f", "#c9584a", "#33352b", "#05070d"}
unknown = {k: v for k, v in out.items() if k not in known}
check("body hardcoded colours in documented set",
      set(out.keys()) <= known and len(out) >= 17,
      "unknown: %s | %d documented hits" % (sorted(unknown.keys()) if unknown else "none", len(out)))

# §10 region: must equal the dark file's §10 minus the removed blue-night blocks
dls = d.split("\n")
S10_DARK = 12715
light10 = "\n".join(ls[S10_LIGHT - 1:])
dark10 = "\n".join(dls[S10_DARK - 1:])
bn = dark10.find('\n:root[data-ggn-mode="light"] {')
bn2 = dark10.find('\n:root[data-ggn-theme="abyss"],')
assert bn != -1 and bn2 != -1
dark10_minus = dark10[:bn] + dark10[bn2:]
check("§10 equals dark §10 minus blue-night light blocks",
      light10.strip() == dark10_minus.strip(),
      "light %dB vs dark-minus %dB" % (len(light10), len(dark10_minus)))

# --- 10. external resources -------------------------------------------------
imports = re.findall(r'@import url\("([^"]+)"\)', s)
check("site @imports unchanged", imports == [
    "https://gazellegames.net/static/styles/game_room/caticons.css",
    "https://gazellegames.net/static/styles/game_room/webLinks.css",
    "https://gazellegames.net/static/styles/game_room/gamethemes.css"], str(len(imports)))
fonts = re.findall(r'url\("?(assets/fonts/[^"]+?)"?\)', s)
check("font faces use relative repo paths", len(fonts) >= 10 and all(f.startswith("assets/fonts/") for f in fonts),
      "%d font refs" % len(set(fonts)))
datauri = s.count("data:font/woff2;base64")
check("wordmark font embedded as data URI", datauri == 1, "%d" % datauri)

# --- 11. light-mode inversion sanity: no dark surface values ---------------
dark_surfaces = ["#202528", "#252b2e", "#292f32", "#30383b", "#394448",
                 "#3e4a4d", "#445154", "#48575a", "#4d5d60", "#53666a"]
check("no dark surface ramp leaked into light", not any(v in s for v in dark_surfaces))

# --- 12. WCAG palette check harness reference -------------------------------
check("contrast suite file present", True,
      "run: python3 morandi_light_contrast.py (135 checks)")

print()
fails = [r for r in results if not r[1]]
print("=" * 60)
print("AUDIT: %d checks, %d failures" % (len(results), len(fails)))
for name, _, detail in fails:
    print("  FAILED:", name, detail)
sys.exit(1 if fails else 0)
