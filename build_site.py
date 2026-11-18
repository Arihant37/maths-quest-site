"""Build the Maths Quest website from the levels Claude has checked by hand. Run on the laptop, then it pushes.

    python build_site.py            # compress new approved levels, rewrite levels.json, commit and push
    python build_site.py --force 3  # recompress level 3 (after a replaced video)

Only levels in youtube_mcp/maths_quest_approved.json are published. The mission answer is stored only as a SHA-256
hash, so the page can check an answer without printing it.
"""
import hashlib
import json
import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import imageio_ffmpeg

PRIYA = Path(r"C:\Users\ariha\Downloads\priya\youtube_mcp")
SITE = Path(__file__).parent


def mission(scenes):
    """(label, kind, answer) from the board of the scene that says 'mission', or None when it cannot be read safely."""
    scene = next((s for s in scenes if "mission" in s["text"].lower()), None)
    if not scene:
        return None
    text = " ".join("".join(p["s"] for p in row) for row in scene["rows"])
    m = re.search(r"(\d+(?:\.\d+)?)\s*([×x*−+÷/-])\s*(\d+(?:\.\d+)?)", text)  # decimals allowed: "100 − 28.43" must not read as "100 − 28"
    if not m:
        return None
    a, op, b = Decimal(m[1]), m[2], Decimal(m[3])

    def show(d):
        return format(d.normalize(), "f")  # 71.570 -> 71.57, 3.8E+2 -> 380

    if op in "×x*":
        return f"{show(a)} × {show(b)}", "number", show(a * b)
    if op == "+":
        return f"{show(a)} + {show(b)}", "number", show(a + b)
    if op in "−-":
        return f"{show(a)} − {show(b)}", "number", show(a - b)
    if op in "÷/":
        return f"Is {show(a)} divisible by {show(b)}?", "yesno", "yes" if a % b == 0 else "no"


def digest(level, answer):
    return hashlib.sha256(f"{level}:{answer}".encode()).hexdigest()


assert mission([{"text": "Your mission: find 72 times 11", "rows": [[{"s": "MISSION"}], [{"s": "72×11 = ?"}]]}]) == ("72 × 11", "number", "792")
assert mission([{"text": "mission", "rows": [[{"s": "5373÷9?"}]]}]) == ("Is 5373 divisible by 9?", "yesno", "yes")
assert mission([{"text": "mission", "rows": [[{"s": "1000 −620 =?"}]]}]) == ("1000 − 620", "number", "380")
assert mission([{"text": "mission", "rows": [[{"s": "100−28.43 = ?"}]]}]) == ("100 − 28.43", "number", "71.57")
assert mission([{"text": "mission", "rows": [[{"s": "72×11 = ?"}]]}]) == ("72 × 11", "number", "792")


def main(force=()):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    approved = json.loads((PRIYA / "maths_quest_approved.json").read_text(encoding="utf-8"))["approved"]
    levels = {l["level"]: l for l in json.loads((PRIYA / "maths_quest_levels.json").read_text(encoding="utf-8"))}
    worlds = list(dict.fromkeys(l["world"] for l in levels.values()))
    out = []
    for n in sorted(approved):
        folder = PRIYA / "out" / "stickman" / f"mq-level-{n:02d}"
        src = folder / f"mq-level-{n:02d}.mp4"
        dst = SITE / "v" / src.name
        if not dst.exists() or n in force:
            subprocess.run([ffmpeg, "-y", "-v", "error", "-i", str(src), "-vf", "scale=540:-2", "-c:v", "libx264", "-crf", "30", "-preset", "medium",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "64k", "-ac", "1", str(dst)], check=True)
        scenes = json.loads((folder / "story.json").read_text(encoding="utf-8"))
        title = (folder / "meta.txt").read_text(encoding="utf-8").splitlines()[0].split("|")[0].strip()
        m = mission(scenes)
        topic = re.split(r" \(a matching", levels[n]["topic"])[0]  # drop internal writing notes
        out.append({"level": n, "world": levels[n]["world"], "world_no": worlds.index(levels[n]["world"]) + 1, "title": title, "lesson": topic,
                    "video": f"v/{src.name}", "seconds": round(scenes[-1]["end"]),
                    "mission": {"label": m[0], "kind": m[1], "hash": digest(n, m[2])} if m else None})
    (SITE / "levels.json").write_text(json.dumps({"total": len(levels), "levels": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(out), "levels on the site;", sum(1 for o in out if not o["mission"]), "without a checkable mission")
    subprocess.run(["git", "add", "-A"], cwd=SITE, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=SITE).returncode:
        subprocess.run(["git", "commit", "-q", "-m", f"Site: {len(out)} checked levels\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01AiafHwitQWKbmbh2PF32Xv"], cwd=SITE, check=True)
        subprocess.run(["git", "push", "-q"], cwd=SITE, check=True)
        print("pushed")


if __name__ == "__main__":
    force = {int(x) for x in sys.argv[sys.argv.index("--force") + 1:]} if "--force" in sys.argv else set()
    main(force)
