"""tokens.json 읽기 · alias 해석 · 대비 계산 공용 함수."""

from __future__ import annotations

import json
import re
from typing import Iterator

NS = "com.unified-ds"
BRANDS = ["NOVERA", "1CHON"]
THEMES = ["Light", "Dark"]
DEFAULT_CTX = {"brand": "NOVERA", "theme": "Light", "scale": "100", "motion": "Default"}


def load(path: str) -> dict:
    return json.load(open(path, encoding="utf-8"))


def meta(tokens: dict) -> dict:
    return tokens["$extensions"][NS]


def iter_tokens(tree: dict, path=()) -> Iterator[tuple[str, dict]]:
    """(figma 이름, 토큰 노드)"""
    for k, v in tree.items():
        if k.startswith("$"):
            continue
        if isinstance(v, dict) and "$value" in v:
            yield v["$extensions"][NS]["name"], v
        elif isinstance(v, dict):
            yield from iter_tokens(v, path + (k,))


def index(tokens: dict) -> dict[str, dict]:
    return dict(iter_tokens(tokens))


REF = re.compile(r"^\{(.+)\}$")


def alias_target(value) -> str | None:
    if isinstance(value, str):
        m = REF.match(value)
        if m:
            return m.group(1).replace(".", "/")
    return None


def pick_mode(tok: dict, collections: dict, ctx: dict) -> str:
    x = tok["$extensions"][NS]
    col = collections[x["collection"]]
    modes = col["modes"]
    axis = col.get("axis")
    if axis and ctx.get(axis) in modes:
        return ctx[axis]
    return modes[0]


def resolve(name: str, idx: dict, collections: dict, ctx: dict, seen=None):
    seen = seen or []
    if name in seen:
        raise ValueError("순환 alias: " + " → ".join(seen + [name]))
    tok = idx.get(name)
    if tok is None:
        raise KeyError(f"alias 대상 없음: {name}")
    mode = pick_mode(tok, collections, ctx)
    val = tok["$extensions"][NS]["modes"].get(mode)
    tgt = alias_target(val)
    if tgt:
        return resolve(tgt, idx, collections, ctx, seen + [name])
    return val


def is_exported(tok: dict) -> bool:
    return not tok["$extensions"][NS]["hidden"]


# ── 색 · 대비 ────────────────────────────────────────────────

def parse_hex(h: str) -> tuple[float, float, float, float]:
    h = h.lstrip("#")
    if len(h) == 6:
        h += "FF"
    r, g, b, a = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4, 6))
    return r, g, b, a


def over(top: str, base: str) -> tuple[float, float, float]:
    r1, g1, b1, a = parse_hex(top)
    r0, g0, b0, _ = parse_hex(base)
    return (r1 * a + r0 * (1 - a), g1 * a + g0 * (1 - a), b1 * a + b0 * (1 - a))


def luminance(rgb) -> float:
    def ch(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str, base: str) -> float:
    bg_rgb = over(bg, base)
    bg_hex = "#" + "".join(f"{round(c * 255):02X}" for c in bg_rgb) + "FF"
    fg_rgb = over(fg, bg_hex)
    l1, l2 = sorted([luminance(fg_rgb), luminance(bg_rgb)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)
