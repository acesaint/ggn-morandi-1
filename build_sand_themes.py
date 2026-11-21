#!/usr/bin/env python3
"""Sand pair stage 2 - controlled theme generation.

Generates ggn-morandi-warm-sand.css from ggn-morandi-warm-paper.css and
ggn-morandi-night-sand.css from ggn-morandi-dark-green.css by pure token
substitution. Allowed edits per file, nothing else:

  1. the file header title line (line 2)
  2. the palette comment line(s) inside the main :root block
  3. the mapped :root token value lines (59 per file)
  4. the --ggn-wm-edge wordmark mix base colour (1 line)

The script refuses to write if the parent diff shows any other change.
Reproducible: run  python3 build_sand_themes.py
"""

import re
import sys

def interp(c1, c2, t):
    h1, h2 = c1.lstrip("#"), c2.lstrip("#")
    out = []
    for i in (0, 2, 4):
        a, b = int(h1[i:i + 2], 16), int(h2[i:i + 2], 16)
        out.append(round(a + (b - a) * t))
    return "#{:02x}{:02x}{:02x}".format(*out)

WARM_SAND = {
    "--surface-0": "#ede9df", "--surface-1": "#e8e3d8", "--surface-2": "#f0ede5",
    "--surface-3": "#f5f2eb", "--surface-4": "#fbf9f4", "--surface-5": "#e9e4d9",
    "--surface-6": "#f7f4ed", "--surface-7": "#faf8f2", "--surface-8": "#fdfcf8",
    "--surface-9": "#ddd6c8",
    "--line-1": "#e1dccf", "--line-2": "#ada591", "--line-3": "#837b68",
    "--line-4": "#7e7767",
    "--surface-deep-rgb": "237, 233, 223", "--surface-2-rgb": "240, 237, 229",
    "--ink-0": "#302b25", "--ink-1": "#39332c", "--ink-2": "#484138",
    "--ink-3": "#574f44", "--ink-4": "#61594d", "--ink-5": "#6a6255",
    "--ink-6": "#706a5b", "--ink-7": "#7c7566", "--ink-8": "#817a6a",
    "--fg-accent": "#7d5335", "--fg-accent-soft": "#8d674b",
    "--fg-good": "#4f6847", "--fg-bad": "#984c3d", "--fg-warn": "#765a22",
    "--fg-bad-soft": "#a05544", "--control": "#626a58", "--on-fill": "#ffffff",
    "--shadow-1": "0 1px 2px rgba(60, 54, 40, 0.06), 0 2px 8px rgba(60, 54, 40, 0.05)",
    "--shadow-2": "0 1px 3px rgba(60, 54, 40, 0.07), 0 6px 20px rgba(60, 54, 40, 0.06)",
    "--shadow-3": "0 2px 6px rgba(60, 54, 40, 0.09), 0 12px 32px rgba(60, 54, 40, 0.08)",
    "--state-leeching": "#4e6b42", "--state-seeding": "#6f6522",
    "--state-uploaded": "#75577d", "--state-snatched": "#9a5644",
    "--cat-stream": "#376b60", "--cat-conference": "#765a22",
    "--cat-birthday": "#7d5a80",
    "--fg-bonus": "#52683d", "--fg-cost": "#765a22", "--fg-error": "#a04a3c",
    "--fg-error-link": "#9e4739", "--fg-report": "#a34a35", "--fg-orange": "#87501d",
}
for _i in range(10):
    WARM_SAND["--ratio-%d" % _i] = interp("#a34a35", "#4f6847", _i / 9.0)

NIGHT_SAND = {
    "--surface-0": "#1d1b18", "--surface-1": "#22201c", "--surface-2": "#25231f",
    "--surface-3": "#302d27", "--surface-4": "#39352e", "--surface-5": "#423e37",
    "--surface-6": "#4f4a42", "--surface-7": "#59534a", "--surface-8": "#635c53",
    "--surface-9": "#68615b",
    "--line-1": "#322f28", "--line-2": "#555045", "--line-3": "#756d60",
    "--line-4": "#948c7f",
    "--surface-deep-rgb": "29, 27, 24", "--surface-2-rgb": "37, 35, 31",
    "--ink-0": "#eae2d5", "--ink-1": "#d8d0c2", "--ink-2": "#cfc7b8",
    "--ink-3": "#c4b8a5", "--ink-4": "#bcb0a0", "--ink-5": "#b0a696",
    "--ink-6": "#a69c8c", "--ink-7": "#928b7b", "--ink-8": "#857e6e",
    "--fg-accent": "#d8a37e", "--fg-accent-soft": "#e0b896",
    "--fg-good": "#a6bd91", "--fg-bad": "#e39a86", "--fg-warn": "#d5b36f",
    "--fg-bad-soft": "#db8e7a", "--control": "#aab49a", "--on-fill": "#1d1b18",
    "--shadow-1": "0 2px 8px rgba(0, 0, 0, 0.16)",
    "--shadow-2": "0 4px 14px rgba(0, 0, 0, 0.2)",
    "--shadow-3": "0 8px 24px rgba(0, 0, 0, 0.24)",
    "--state-leeching": "#a6bd91", "--state-seeding": "#d5b36f",
    "--state-uploaded": "#c9b4c4", "--state-snatched": "#dca28e",
    "--cat-stream": "#a3bdb2", "--cat-conference": "#d2bc8e",
    "--cat-birthday": "#cbb3c4",
    "--fg-bonus": "#b7c49c", "--fg-cost": "#d2bc8e", "--fg-error": "#e5a79a",
    "--fg-error-link": "#edbcae", "--fg-report": "#dca28e", "--fg-orange": "#dca87e",
}
for _i in range(10):
    NIGHT_SAND["--ratio-%d" % _i] = interp("#dca28e", "#a6bd91", _i / 9.0)

# sanity: ratio ramps must equal the contrast-suite interpolation
for i in range(10):
    t = i / 9.0
    assert WARM_SAND["--ratio-%d" % i] == interp("#a34a35", "#4f6847", t), i
    assert NIGHT_SAND["--ratio-%d" % i] == interp("#dca28e", "#a6bd91", t), i

JOBS = [
    {
        "parent": "ggn-morandi-warm-paper.css",
        "child": "ggn-morandi-warm-sand.css",
        "tokens": WARM_SAND,
        "header_old": "   GGN Morandi Warm Paper — light Morandi theme for GazelleGames",
        "header_new": "   GGN Morandi Warm Sand — light Morandi theme for GazelleGames",
        "comment_old": "  /* Warm-paper light Morandi palette; see MORANDI_LIGHT_TOKENS.md. */",
        "comment_new": "  /* Warm-sand light Morandi palette; see SAND_THEME_TOKENS.md. */",
        "wm_old": "  --ggn-wm-edge: color-mix(in srgb, var(--fg-accent) 22%, #33352b);",
        "wm_new": "  --ggn-wm-edge: color-mix(in srgb, var(--fg-accent) 22%, #302b25);",
        "purgelines": 1,
    },
    {
        "parent": "ggn-morandi-dark-green.css",
        "child": "ggn-morandi-night-sand.css",
        "tokens": NIGHT_SAND,
        "header_old": "   GGN Morandi Dark Green — muted Morandi deep-green theme for GazelleGames",
        "header_new": "   GGN Morandi Night Sand — warm charcoal dark Morandi theme for GazelleGames",
        "comment_old": ("  /* Dark Morandi palette (phase 3): surfaces, inks, lines keep their\n"
                        "     original ramp semantics; see MORANDI_DESIGN_TOKENS.md. */"),
        "comment_new": ("  /* Night-sand dark Morandi palette (sand pair): surfaces, inks, lines\n"
                        "     keep their original ramp semantics; see SAND_THEME_TOKENS.md. */"),
        "wm_old": "  --ggn-wm-edge: color-mix(in srgb, var(--fg-accent) 22%, #05070d);",
        "wm_new": "  --ggn-wm-edge: color-mix(in srgb, var(--fg-accent) 22%, #14110d);",
        "purgelines": 2,
    },
]

for job in JOBS:
    src = open(job["parent"]).read().split("\n")
    out = list(src)

    # 1. header title
    assert src[1] == job["header_old"], "header mismatch: %r" % src[1]
    out[1] = job["header_new"]

    # 2. locate main :root block (contains --ggn-bg)
    root_start = None
    for i, ln in enumerate(src):
        if ln == ":root {" and "--ggn-bg" in "\n".join(src[i:i + 4]):
            root_start = i
            break
    assert root_start is not None, "main :root not found"
    root_end = next(i for i in range(root_start + 1, len(src)) if src[i] == "}")

    # palette comment lines
    comment_lines = job["comment_old"].split("\n")
    assert src[root_start + 2:root_start + 2 + len(comment_lines)] == comment_lines, \
        "palette comment mismatch at root block"
    out[root_start + 2:root_start + 2 + len(comment_lines)] = job["comment_new"].split("\n")

    # 3. token substitutions inside the block
    changed = 0
    for i in range(root_start + 1, root_end):
        m = re.match(r"^  (--[\w-]+): (.*);$", src[i])
        if not m:
            continue
        name = m.group(1)
        if name in job["tokens"]:
            assert src[i] == "  %s: %s;" % (name, m.group(2))
            out[i] = "  %s: %s;" % (name, job["tokens"][name])
            changed += 1
    assert changed == 59, "expected 59 token lines, changed %d" % changed

    # 4. wordmark edge base
    wm_idx = [i for i, ln in enumerate(src) if ln == job["wm_old"]]
    assert len(wm_idx) == 1, "wordmark line not found"
    out[wm_idx[0]] = job["wm_new"]

    # line count must be identical
    assert len(out) == len(src)

    # verify: diff parent vs child hits ONLY the whitelisted lines
    changed_lines = [i for i in range(len(src)) if src[i] != out[i]]
    allowed = {1} | set(range(root_start + 2, root_start + 2 + job["purgelines"])) \
              | {wm_idx[0]}
    token_changed = [i for i in range(root_start + 1, root_end)
                     if re.match(r"^  (--[\w-]+): (.*);$", src[i])
                     and re.match(r"^  (--[\w-]+): (.*);$", src[i]).group(1) in job["tokens"]]
    allowed |= set(token_changed)
    unexpected = [i for i in changed_lines if i not in allowed]
    assert not unexpected, "unexpected changed lines: %r" % unexpected[:5]
    print("%s: %d lines changed (header 1 + comment %d + tokens %d + wordmark 1)"
          % (job["child"], len(changed_lines), job["purgelines"], changed))

    with open(job["child"], "w") as f:
        f.write("\n".join(out))

print("both themes written and diff-verified")
