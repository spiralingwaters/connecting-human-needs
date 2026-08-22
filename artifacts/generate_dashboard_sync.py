#!/usr/bin/env python3
"""Sync the dashboard's Feature List and Thoughts mirrors from their source files.

Run this any time FeaturesList.md gains/loses a bullet, or a Thoughts/*.md
file gets rewritten, and you want artifacts/dashboard.html to catch up:

    python3 artifacts/generate_dashboard_sync.py

It derives state.features[].text/done from FeaturesList.md and
state.thoughts[].text from Thoughts/*.md, and writes them back into the
#dashboard-data JSON already embedded in artifacts/dashboard.html — purely
mechanical, no rewriting/summarizing. Every other field (notes, settings,
missionStatement, quickOptions, graphicsSuggestions, graphicsCustomText,
graphics, and the interactive parts of features/thoughts: picked and
newDreamRequested) is left exactly as found, matched up by id so those
flags survive the sync.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD = REPO_ROOT / "artifacts" / "dashboard.html"
FEATURES_MD = REPO_ROOT / "FeaturesList.md"

THOUGHT_FILES = [
    ("one", "Thoughts/ThoughtOne.md"),
    ("two", "Thoughts/ThoughtTwo.md"),
    ("three", "Thoughts/ThoughtThree.md"),
]

DATA_SCRIPT_RE = re.compile(
    r'(<script id="dashboard-data" type="application/json">)(.*?)(</script>)',
    re.S,
)

FEATURE_LINE_RE = re.compile(r"^-\s+\[( |x|X)\]\s+(.*\S)\s*$")


def feature_id(text):
    return "f" + hashlib.sha1(text.encode("utf-8")).hexdigest()[:14]


def parse_features_md():
    features = []
    for line in FEATURES_MD.read_text(encoding="utf-8").splitlines():
        m = FEATURE_LINE_RE.match(line)
        if not m:
            continue
        done = m.group(1).lower() == "x"
        text = m.group(2)
        features.append({"id": feature_id(text), "text": text, "done": done})
    return features


def load_thought_text(rel_path):
    full = REPO_ROOT / rel_path
    return full.read_text(encoding="utf-8").strip()


def sync_features(existing_features, parsed_features):
    picked_by_id = {f["id"]: f.get("picked", False) for f in existing_features}
    return [
        {
            "id": f["id"],
            "text": f["text"],
            "done": f["done"],
            "picked": False if f["done"] else picked_by_id.get(f["id"], False),
        }
        for f in parsed_features
    ]


def sync_thoughts(existing_thoughts):
    existing_by_id = {t["id"]: t for t in existing_thoughts}
    synced = []
    for tid, rel_path in THOUGHT_FILES:
        prev = existing_by_id.get(tid, {})
        synced.append(
            {
                "id": tid,
                "file": rel_path,
                "text": load_thought_text(rel_path),
                "newDreamRequested": bool(prev.get("newDreamRequested", False)),
            }
        )
    return synced


def main():
    html = DASHBOARD.read_text(encoding="utf-8")
    m = DATA_SCRIPT_RE.search(html)
    if not m:
        print("Could not find #dashboard-data script in artifacts/dashboard.html", file=sys.stderr)
        return 1

    state = json.loads(m.group(2))
    parsed_features = parse_features_md()
    state["features"] = sync_features(state.get("features", []), parsed_features)
    state["thoughts"] = sync_thoughts(state.get("thoughts", []))

    new_json = json.dumps(state, separators=(",", ":")).replace("</", "<\\/")
    new_html = html[: m.start()] + m.group(1) + new_json + m.group(3) + html[m.end() :]
    DASHBOARD.write_text(new_html, encoding="utf-8")

    print(f"Synced {len(state['features'])} feature(s) from FeaturesList.md")
    print(f"Synced {len(state['thoughts'])} thought(s) from Thoughts/*.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
