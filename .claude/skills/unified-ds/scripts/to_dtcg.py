#!/usr/bin/env python3
"""Figma 원시 변수 JSON → tokens.json (W3C DTCG).

    python3 to_dtcg.py build/raw-variables.json -o tokens.json [--version 1.3.0]

- 이름의 `/` 를 DTCG 그룹 중첩으로 바꾼다(`bg/neutral-solid` → bg › neutral-solid).
- `$value` 는 첫 모드 값, 모드별 값은 `$extensions["com.unified-ds"].modes` 에.
- alias 는 DTCG 참조 문법 `{bg.neutral-solid}`.
- 컬렉션 → role 매핑은 COLLECTION_ROLES. 모르는 컬렉션은 role "unknown" 으로 두고 린트가 잡는다.
- tokens.json 은 생성물이다. 손으로 고치지 않는다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

NS = "com.unified-ds"

# Figma 컬렉션 이름(소문자, 공백·기호 제거 후 접두 일치) → role
COLLECTION_ROLES = [
    ("primitive", "primitive"),
    ("brand", "brand"),
    ("semantic", "semantic"),
    ("module", "module"),
    ("commerce", "module"),
    ("messenger", "module"),
    ("spacing", "spacing"),
    ("radius", "radius"),
    ("borderwidth", "border-width"),
    ("typography", "typography"),
    ("elevation", "elevation"),
    ("motion", "motion"),
]

ROLE_AXIS = {
    "brand": "brand", "semantic": "theme", "module": "theme", "elevation": "theme",
    "typography": "scale", "motion": "motion",
}


def role_of(collection: str) -> str:
    key = re.sub(r"[^a-z]", "", collection.lower())
    for prefix, role in COLLECTION_ROLES:
        if key.startswith(prefix):
            return role
    return "unknown"


def dtcg_type(name: str, figma_type: str) -> str:
    if figma_type == "COLOR":
        return "color"
    if figma_type == "STRING":
        if name.startswith("font/family/"):
            return "fontFamily"
        return "string"
    if figma_type == "BOOLEAN":
        return "boolean"
    if name.startswith("motion/duration/"):
        return "duration"
    if re.match(r"(spacing|space|radius|border-width|font/size)/", name):
        return "dimension"
    return "number"


def ref(value):
    if isinstance(value, dict) and "alias" in value:
        if value["alias"] is None:
            return "{__unresolved__." + value.get("aliasId", "?") + "}"
        return "{" + value["alias"].replace("/", ".") + "}"
    return value


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("-o", "--out", default="tokens.json")
    ap.add_argument("--version", default="0.0.0")
    a = ap.parse_args()

    raw = json.load(open(a.raw, encoding="utf-8"))
    tree: dict = {}
    collections = {}
    for c in raw["collections"]:
        role = role_of(c["name"])
        collections[c["name"]] = {
            "role": role, "modes": c["modes"], "hidden": c.get("hidden", False),
            "axis": ROLE_AXIS.get(role), "count": c.get("count"),
        }

    dup = []
    for v in sorted(raw["variables"], key=lambda x: x["name"]):
        col = collections[v["collection"]]
        modes = {m: ref(v["values"].get(m)) for m in col["modes"]}
        first = modes[col["modes"][0]]
        node = tree
        parts = v["name"].split("/")
        for p in parts[:-1]:
            node = node.setdefault(p, {})
            if "$value" in node:
                dup.append(v["name"])
        if parts[-1] in node:
            dup.append(v["name"])
        node[parts[-1]] = {
            "$type": dtcg_type(v["name"], v["type"]),
            "$value": first,
            **({"$description": v["description"]} if v["description"] else {}),
            "$extensions": {NS: {
                "name": v["name"],
                "collection": v["collection"],
                "role": col["role"],
                "modes": modes,
                "scopes": v["scopes"],
                "hidden": bool(v["hidden"] or col["hidden"] or col["role"] == "primitive"),
                "figmaId": v["id"],
            }},
        }

    out = {
        "$extensions": {NS: {
            "version": a.version,
            "fileKey": raw.get("fileKey"),
            "extractedAt": raw.get("extractedAt"),
            "collections": collections,
        }},
        **tree,
    }
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{a.out}: 변수 {len(raw['variables'])}개, 컬렉션 {len(collections)}개")
    if dup:
        print(f"경고: 그룹/토큰 이름 충돌 {len(dup)}건 — {dup[:5]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
