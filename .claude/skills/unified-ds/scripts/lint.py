#!/usr/bin/env python3
"""검증 린트 — SKILL.md 체크리스트 1–7.

    python3 lint.py --tokens tokens.json \
        [--spec spec.json]            # 생성 전 사전 검증: 스펙을 tokens 에 합쳐 검사
        [--css dist/react/tokens.css] [--dart dist/flutter/lib/tokens.g.dart] \
        [--src src/ lib/]             # 폐기 토큰 사용처 · hex/px 리터럴 스캔
        [--figma-count 363]           # 패리티: Figma 공개 변수 수
        [--json]

종료 코드 0 = 통과, 1 = 실패. 경고는 통과에 영향 없음.
spec.json 은 tokens.json 과 같은 모양(DTCG 트리)이다. 이름이 같으면 spec 이 덮어쓴다.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

from naming import check_name, to_code, to_css
from tokens_lib import (BRANDS, DEFAULT_CTX, NS, THEMES, alias_target, contrast, index,
                        is_exported, load, meta, resolve)

HERE = os.path.dirname(os.path.abspath(__file__))

SCOPES = [  # (접두사, 반드시 포함, 허용 집합)
    (r"(commerce/|messenger/)?bg/", {"FRAME_FILL", "SHAPE_FILL"}, {"FRAME_FILL", "SHAPE_FILL"}),
    (r"(commerce/|messenger/)?fg/", {"TEXT_FILL", "SHAPE_FILL", "STROKE_COLOR"}, {"TEXT_FILL", "SHAPE_FILL", "STROKE_COLOR"}),
    (r"(commerce/|messenger/)?stroke/", {"STROKE_COLOR"}, {"STROKE_COLOR"}),
    (r"spacing/|space/", {"GAP"}, {"GAP", "WIDTH_HEIGHT"}),
    (r"radius/", {"CORNER_RADIUS"}, {"CORNER_RADIUS"}),
    (r"border-width/", {"STROKE_FLOAT"}, {"STROKE_FLOAT"}),
    (r"font/size/", {"FONT_SIZE"}, {"FONT_SIZE"}),
    (r"font/family/", {"FONT_FAMILY"}, {"FONT_FAMILY"}),
]


class Report:
    def __init__(self):
        self.items: list[tuple[str, str, str]] = []

    def err(self, check, msg):
        self.items.append(("FAIL", check, msg))

    def warn(self, check, msg):
        self.items.append(("WARN", check, msg))

    @property
    def failed(self):
        return any(s == "FAIL" for s, _, _ in self.items)


def merge(base: dict, spec: dict) -> dict:
    out = json.loads(json.dumps(base))
    def walk(dst, src):
        for k, v in src.items():
            if k.startswith("$") and dst is out:
                continue
            if isinstance(v, dict) and "$value" not in v and isinstance(dst.get(k), dict):
                walk(dst[k], v)
            else:
                dst[k] = v
    walk(out, spec)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--spec")
    ap.add_argument("--css")
    ap.add_argument("--dart")
    ap.add_argument("--src", nargs="*", default=[])
    ap.add_argument("--figma-count", type=int)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    tokens = load(a.tokens)
    if a.spec:
        tokens = merge(tokens, load(a.spec))
    cols = meta(tokens)["collections"]
    idx = index(tokens)
    R = Report()

    # 0. 컬렉션 구조
    for cname, c in cols.items():
        if c["role"] == "unknown":
            R.err("구조", f"컬렉션 '{cname}' 은 규칙에 없는 컬렉션 (references/collections.md)")
        if c["role"] == "primitive" and not c.get("hidden"):
            R.warn("구조", f"Primitive 컬렉션 '{cname}' 이 hiddenFromPublishing 아님")
        if c["role"] == "brand" and set(c["modes"]) != set(BRANDS):
            R.warn("구조", f"Brand 모드 {c['modes']} ≠ {BRANDS} — 서비스 추가는 사용자 확인 필요")
        if c["role"] in ("semantic", "module") and c["modes"] != THEMES:
            R.err("구조", f"'{cname}' 모드 {c['modes']} ≠ {THEMES}")

    for name, tok in idx.items():
        x = tok["$extensions"][NS]
        role = x["role"]
        col = cols[x["collection"]]

        # 1. 이름
        for m in check_name(name, role):
            R.err("이름", m)

        # 2. 참조
        for mode, val in x["modes"].items():
            tgt = alias_target(val)
            if role in ("semantic", "module"):
                if not tgt:
                    R.err("참조", f"{name} [{mode}]: 직접 값 {val!r} — alias 만 허용")
                    continue
            if not tgt:
                continue
            t = idx.get(tgt)
            if t is None:
                R.err("참조", f"{name} [{mode}]: alias 대상 '{tgt}' 없음")
                continue
            trole = t["$extensions"][NS]["role"]
            if role == "semantic" and trole not in ("primitive", "brand"):
                R.err("참조", f"{name} → {tgt}: Semantic 은 Primitive/Brand 만 참조 ({trole})")
            if role == "module":
                if trole != "semantic":
                    R.err("참조", f"{name} → {tgt}: Module 은 Semantic 만 참조 ({trole})")
                if tgt.split("/")[0] in ("commerce", "messenger"):
                    R.err("참조", f"{name} → {tgt}: 모듈 간 참조 금지")

        # 3. 모드 완성도
        for mode in col["modes"]:
            if x["modes"].get(mode) in (None, ""):
                R.err("모드", f"{name}: 모드 '{mode}' 값 없음")

        # 5. scope
        scopes = set(x.get("scopes") or [])
        if "ALL_SCOPES" in scopes:
            R.err("scope", f"{name}: ALL_SCOPES 금지")
        elif role not in ("primitive",) and not name.startswith("brand/"):
            for pat, must, allowed in SCOPES:
                if re.match(pat, name):
                    if not must <= scopes and not (pat.startswith("spacing") and "GAP" in scopes):
                        R.err("scope", f"{name}: {sorted(scopes)} — 필요 {sorted(must)}")
                    elif scopes - allowed:
                        R.warn("scope", f"{name}: 허용 밖 scope {sorted(scopes - allowed)}")
                    break

        # 7. 폐기
        if tok.get("$description", "").lower().startswith("deprecated"):
            R.warn("폐기", f"{name}: {tok['$description']}")

    # 4. 대비
    pairs = json.load(open(os.path.join(HERE, "contrast_pairs.json"), encoding="utf-8"))
    for b in BRANDS:
        for th in THEMES:
            ctx = {**DEFAULT_CTX, "brand": b, "theme": th}
            try:
                base = resolve(pairs["composite_base"], idx, cols, ctx)
            except Exception:
                R.warn("대비", f"[{b}/{th}] 기준 배경 {pairs['composite_base']} 없음 — 대비 검사 생략")
                break
            for p in pairs["pairs"]:
                if p["fg"] not in idx or p["bg"] not in idx:
                    continue
                try:
                    fg = resolve(p["fg"], idx, cols, ctx)
                    bg = resolve(p["bg"], idx, cols, ctx)
                except Exception as e:
                    R.err("대비", f"[{b}/{th}] {p['fg']} on {p['bg']}: 해석 실패 {e}")
                    continue
                r = contrast(fg, bg, base)
                if r < p["min"]:
                    R.err("대비", f"[{b}/{th}] {p['fg']} on {p['bg']}: {r:.2f} < {p['min']}")

    # 6. 패리티
    exported = sorted(n for n, t in idx.items() if is_exported(t))
    counts = {"tokens.json(공개)": len(exported)}
    if a.figma_count is not None:
        counts["Figma"] = a.figma_count
    if a.css:
        css = open(a.css, encoding="utf-8").read()
        names = set(re.findall(r"(--[\w-]+)\s*:", css))
        counts["CSS"] = len(names)
        missing = [n for n in exported if to_css(n) not in names]
        if missing:
            R.err("패리티", f"CSS 에 없는 토큰 {len(missing)}개: {missing[:5]}")
        dup = {}
        for n in exported:
            dup.setdefault(to_css(n), []).append(n)
        for k, v in dup.items():
            if len(v) > 1:
                R.err("패리티", f"CSS 이름 충돌 {k}: {v}")
    if a.dart:
        dart = open(a.dart, encoding="utf-8").read()
        fields = re.findall(r"^  final (?:Color|double|Duration|String|bool|Object) (\w+);", dart, re.M)
        counts["Dart"] = len(fields)
        seen = {}
        for n in exported:
            g, k = to_code(n)
            seen.setdefault((g, k), []).append(n)
        for k, v in seen.items():
            if len(v) > 1:
                R.err("패리티", f"코드 이름 충돌 {'.'.join(k)}: {v}")
    if len(set(counts.values())) > 1:
        R.err("패리티", f"개수 불일치 {counts}")

    # 7. 폐기 사용처 + 리터럴
    deprecated = [n for n, t in idx.items() if t.get("$description", "").lower().startswith("deprecated")]
    needles = {n: [to_css(n), ".".join(to_code(n))] for n in deprecated}
    for root in a.src:
        for dp, _, fs in os.walk(root):
            if "node_modules" in dp or "/build" in dp or "/dist" in dp:
                continue
            for f in fs:
                if not f.endswith((".ts", ".tsx", ".js", ".jsx", ".css", ".dart")) or ".g." in f:
                    continue
                p = os.path.join(dp, f)
                body = open(p, encoding="utf-8", errors="ignore").read()
                for n, keys in needles.items():
                    if any(k in body for k in keys):
                        R.warn("폐기", f"{p}: Deprecated 토큰 {n} 사용")
                if f.endswith((".tsx", ".jsx", ".ts")) and "tokens" not in f:
                    for m in re.finditer(r"#[0-9a-fA-F]{3,8}\b|\b\d+px\b", body):
                        R.err("리터럴", f"{p}: 컴포넌트 코드의 hex/px 리터럴 '{m.group(0)}'")
                        break

    if a.json:
        print(json.dumps([{"level": s, "check": c, "msg": m} for s, c, m in R.items], ensure_ascii=False, indent=2))
    else:
        by = {}
        for s, c, m in R.items:
            by.setdefault(c, []).append((s, m))
        for c, ms in by.items():
            print(f"── {c} ({sum(1 for s, _ in ms if s == 'FAIL')} 실패 · {sum(1 for s, _ in ms if s == 'WARN')} 경고)")
            for s, m in ms[:40]:
                print(f"  {s}  {m}")
            if len(ms) > 40:
                print(f"  … 외 {len(ms) - 40}건")
        print(f"\n패리티 {counts}")
        print("결과:", "실패" if R.failed else "통과")
    return 1 if R.failed else 0


if __name__ == "__main__":
    sys.exit(main())
