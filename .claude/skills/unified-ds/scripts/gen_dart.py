#!/usr/bin/env python3
"""해석본 4개 → Flutter ThemeExtension Dart 코드.

    python3 gen_dart.py build/resolved -o dist/flutter/lib/tokens.g.dart

생성물
- 그룹(bg · fg · stroke · commerce · spacing · radius · font …)마다 `{Group}Tokens` 클래스
- 묶음 `AppTokens extends ThemeExtension<AppTokens>` + 브랜드×테마 인스턴스 4개
  (`AppTokens.noveraLight` …)
- `extension AppTokensX on BuildContext { AppTokens get tokens }` → `context.tokens.bg.neutralSolid`
- Motion Reduced 대응: `context.motionDuration(context.tokens.motion.duration200)`
  → `MediaQuery.disableAnimationsOf(context)` 가 true 면 Duration.zero
- Typography 스케일 모드(100·110·120·135%)는 `AppTextScale` 상수 → `TextScaler.linear()`

이름은 Figma 와 동일(naming.to_code). ColorScheme 에 끼워 맞추지 않는다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from naming import to_code
from tokens_lib import NS

COMBOS = [("novera", "light"), ("novera", "dark"), ("1chon", "light"), ("1chon", "dark")]
SCALES = {"s100": 1.0, "s110": 1.1, "s120": 1.2, "s135": 1.35}


def flat(tree: dict) -> dict[str, dict]:
    out = {}
    for k, v in tree.items():
        if isinstance(v, dict) and "$value" in v:
            out[v["$extensions"][NS]["name"]] = v
        elif isinstance(v, dict):
            out.update(flat(v))
    return out


def dart_type(t: str) -> str:
    return {"color": "Color", "dimension": "double", "number": "double",
            "duration": "Duration", "fontFamily": "String", "string": "String",
            "boolean": "bool"}.get(t, "Object")


def dart_value(t: str, v) -> str:
    if t == "color":
        h = v.lstrip("#").upper()
        h = h if len(h) == 8 else h + "FF"
        return f"Color(0x{h[6:8]}{h[0:6]})"
    if t in ("dimension", "number"):
        return f"{float(v)}"
    if t == "duration":
        return f"Duration(milliseconds: {int(v)})"
    if t == "boolean":
        return "true" if v else "false"
    return json.dumps(str(v), ensure_ascii=False)


def lerp(t: str, f: str) -> str:
    if t == "Color":
        return f"Color.lerp({f}, other.{f}, t)!"
    if t == "double":
        return f"lerpDouble({f}, other.{f}, t)!"
    return f"t < 0.5 ? {f} : other.{f}"


def pascal(s: str) -> str:
    s = s[0].upper() + s[1:]
    return "N" + s[1:] if s[0].isdigit() else s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("resolved_dir")
    ap.add_argument("-o", "--out", default="dist/flutter/lib/tokens.g.dart")
    a = ap.parse_args()

    data = {}
    for b, th in COMBOS:
        data[(b, th)] = flat(json.load(open(os.path.join(a.resolved_dir, f"{b}-{th}.json"), encoding="utf-8")))
    names = sorted(data[COMBOS[0]])
    for k, d in data.items():
        if sorted(d) != names:
            print(f"조합 {k} 의 토큰 집합이 다르다", file=sys.stderr)
            return 1

    groups: dict[str, list[tuple[str, str, str]]] = {}
    for n in names:
        g, key = to_code(n)
        groups.setdefault(g, []).append((key, n, data[COMBOS[0]][n]["$type"]))

    L = ["// 생성 파일 — 수정 금지. 원본은 Figma Variables (unified-ds 스킬).",
         "// ignore_for_file: constant_identifier_names", "",
         "import 'dart:ui' show lerpDouble;", "import 'package:flutter/material.dart';", ""]

    for g, fields in groups.items():
        cls = pascal(g) + "Tokens"
        L.append(f"@immutable\nclass {cls} {{")
        L.append(f"  const {cls}({{" + " ".join(f"required this.{k}," for k, _, _ in fields) + "});")
        for k, n, t in fields:
            L.append(f"  /// `{n}`\n  final {dart_type(t)} {k};")
        L.append(f"  {cls} lerp({cls} other, double t) => {cls}(")
        for k, _, t in fields:
            L.append(f"    {k}: {lerp(dart_type(t), k)},")
        L.append("  );\n}\n")

    L.append("@immutable\nclass AppTokens extends ThemeExtension<AppTokens> {")
    L.append("  const AppTokens({" + " ".join(f"required this.{g}," for g in groups) + "});")
    for g in groups:
        L.append(f"  final {pascal(g)}Tokens {g};")
    L.append("\n  @override\n  AppTokens copyWith() => this;\n")
    L.append("  @override\n  AppTokens lerp(ThemeExtension<AppTokens>? other, double t) {")
    L.append("    if (other is! AppTokens) return this;")
    L.append("    return AppTokens(" + " ".join(f"{g}: {g}.lerp(other.{g}, t)," for g in groups) + ");\n  }\n")
    for b, th in COMBOS:
        inst = ("n" + b if b[0].isdigit() else b) + th.capitalize()
        L.append(f"  static const {inst} = AppTokens(")
        for g, fields in groups.items():
            L.append(f"    {g}: {pascal(g)}Tokens(")
            for k, n, t in fields:
                L.append(f"      {k}: {dart_value(t, data[(b, th)][n]['$value'])},")
            L.append("    ),")
        L.append("  );\n")
    L.append("  static AppTokens of(String brand, Brightness b) => switch ((brand, b)) {")
    for b, th in COMBOS:
        inst = ("n" + b if b[0].isdigit() else b) + th.capitalize()
        L.append(f"    ('{b}', Brightness.{th}) => {inst},")
    L.append("    _ => noveraLight,\n  };\n}\n")

    L.append("/// Typography 스케일 모드 → TextScaler.linear(AppTextScale.s120)")
    L.append("abstract final class AppTextScale {")
    for k, v in SCALES.items():
        L.append(f"  static const double {k} = {v};")
    L.append("}\n")

    L.append("extension AppTokensX on BuildContext {")
    L.append("  AppTokens get tokens => Theme.of(this).extension<AppTokens>() ?? AppTokens.noveraLight;")
    L.append("  /// Motion Reduced 모드 — 시스템 '애니메이션 줄이기'면 0")
    L.append("  Duration motionDuration(Duration d) =>")
    L.append("      MediaQuery.disableAnimationsOf(this) ? Duration.zero : d;")
    L.append("}")

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"{a.out}: 그룹 {len(groups)}개, 필드 {len(names)}개")
    return 0


if __name__ == "__main__":
    sys.exit(main())
