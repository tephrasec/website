#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Writes data/rules.json from a Tephra checkout's rules/*.yaml, so the
rules page lists exactly the rules that ship. Usage: rules.py <tephra dir>"""
import glob
import json
import os
import re
import sys

import yaml

TACTICS = {
    "initial_access": "Initial access", "execution": "Execution", "persistence": "Persistence",
    "privilege_escalation": "Privilege escalation", "defense_evasion": "Defense evasion",
    "credential_access": "Credential access", "discovery": "Discovery",
    "lateral_movement": "Lateral movement", "collection": "Collection",
    "command_and_control": "Command and control", "exfiltration": "Exfiltration", "impact": "Impact",
}


def main(tephra):
    out = []
    for path in sorted(glob.glob(os.path.join(tephra, "rules", "*.yaml"))):
        with open(path) as f:
            r = yaml.safe_load(f)
        tags = r.get("tags", [])
        tactics = [TACTICS.get(t.split(".", 1)[1], t) for t in tags if not re.match(r"attack\.t\d", t)]
        techniques = [t.split(".", 1)[1].upper() for t in tags if re.match(r"attack\.t\d", t)]
        out.append({
            "id": r["id"],
            "title": r["title"],
            "level": r.get("level", ""),
            "event": r.get("event") or "sequence",
            "action": r.get("action", "alert"),
            "tactics": tactics,
            "techniques": techniques,
            "description": " ".join(str(r.get("description", "")).split()),
            "falsepositives": [" ".join(str(x).split()) for x in r.get("falsepositives", []) or []],
            "file": "rules/" + os.path.basename(path),
        })
    if not out:
        sys.exit("no rules found under " + tephra)
    os.makedirs("data", exist_ok=True)
    with open("data/rules.json", "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    print(f"{len(out)} rules")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../Tephra")
