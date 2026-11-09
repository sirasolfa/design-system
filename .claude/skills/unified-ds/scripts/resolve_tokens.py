#!/usr/bin/env python3
"""tokens.json → 브랜드 × 테마 해석본 4개.

    python3 resolve_tokens.py tokens.json -o build/resolved

출력: build/resolved/{brand}-{theme}.json (예: novera-light.json)
- 공개 토큰(hidden 아님)만 담는다. Primitive 는 hidden 이므로 빠진다.
- 값은 alias 를 끝까지 따라간 리터럴. 구조는 DTCG 그대로라 Style Dictionary 가 바로 읽는다.
- Typography 는 scale=100, Motion 은 Default 모드로 해석한다(배율·Reduced 는 런타임).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from tokens_lib import BRANDS, DEFAULT_CTX, NS, THEMES, index, is_exported, load, meta, resolve


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tokens")
    ap.add_argument("-o", "--out", default="build/resolved")
    a = ap.parse_args()

    tokens = load(a.tokens)
    cols = meta(tokens)["collections"]
    idx = index(tokens)
    os.makedirs(a.out, exist_ok=True)
    errors = []
    for brand in BRANDS:
        for theme in THEMES:
            ctx = {**DEFAULT_CTX, "brand": brand, "theme": theme}
            tree: dict = {}
            n = 0
            for name, tok in idx.items():
                if not is_exported(tok):
                    continue
                try:
                    val = resolve(name, idx, cols, ctx)
                except (KeyError, ValueError) as e:
                    errors.append(f"[{brand}/{theme}] {name}: {e}")
                    continue
                node = tree
                parts = name.split("/")
                for p in parts[:-1]:
                    node = node.setdefault(p, {})
                node[parts[-1]] = {
                    "$type": tok["$type"],
                    "$value": val,
                    **({"$description": tok["$description"]} if "$description" in tok else {}),
                    "$extensions": {NS: {"name": name}},
                }
                n += 1
            fn = os.path.join(a.out, f"{brand.lower()}-{theme.lower()}.json")
            json.dump(tree, open(fn, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print(f"{fn}: {n}개")
    if errors:
        print(f"해석 실패 {len(errors)}건:", *errors[:20], sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
