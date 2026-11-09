"""이름 문법과 플랫폼 변환 — 모든 스크립트가 이 모듈 하나를 쓴다.

references/naming.md 와 1:1 대응. 어휘를 바꾸려면 두 곳을 함께 고친다(어휘 추가는 결정 안건).
"""

from __future__ import annotations

import re

PROPERTIES = ["bg", "fg", "stroke"]
TONES = ["layer", "neutral", "brand", "informative", "positive", "warning",
         "critical", "disabled", "overlay", "state"]
EMPHASES = ["solid", "weak", "subtle", "muted", "placeholder", "contrast", "strong"]
STATES = ["hover", "pressed", "selected"]
LAYER_QUALIFIERS = ["default", "basement", "floating", "fill"]   # tone=layer 바로 뒤에서만
STROKE_ONLY_TONES = ["focus"]                                     # property=stroke 일 때만
MODULES = ["commerce", "messenger"]
FOUR_TONES = ["informative", "positive", "warning", "critical"]
BRAND_RAMPS = ["primary", "secondary"]
BRAND_STEPS = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"]

# 컴포넌트명이 든 토큰 금지 — 통합 DS 페이지 목록(references/assets.md) 기준, 소문자 비교
COMPONENT_WORDS = {
    "button", "iconbutton", "textbutton", "buttongroup", "link", "fab", "speeddial",
    "textfield", "textarea", "search", "select", "dropdown", "inputbutton", "field",
    "checkbox", "radio", "switch", "slider", "chip", "segmentedcontrol", "datepicker",
    "timepicker", "quantitypicker", "pincode", "keypad", "attachmentinput", "attachmentchip",
    "imagecheck", "card", "listcell", "listheader", "sectionheader", "avatar", "avatargroup",
    "thumbnail", "accordion", "divider", "badge", "contentbadge", "pushbadge", "label",
    "taggroup", "callout", "banner", "opengraph", "gallerygriditem", "imagelightbox",
    "videoplayer", "topappbar", "bottomnav", "sidebar", "tabs", "tab", "menu", "pagination",
    "dotpagination", "progresstracker", "breadcrumb", "loading", "skeleton", "progressbar",
    "emptystate", "statelayer", "scrollfog", "dialog", "alertdialog", "bottomsheet", "drawer",
    "snackbar", "toast", "tooltip", "productcard", "price", "optionrow", "table", "carousel",
    "footer", "buttonactionbar", "socialloginbutton", "stepper", "messagebubble",
    "messagecomposer", "messagestatus", "chatlistitem", "chatroomsidepanel", "reaction",
    "reactionpicker", "quickreactiontoolbar", "emoticonpicker", "typeindicator",
    "unreaddivider", "dateseparator", "systemmessage", "replypreview", "voicememoplayer",
    "newmessagefab", "photocommentcell", "profilecard", "bubble", "toolbar", "chat",
}

NON_COLOR_PATTERNS = [
    r"spacing/\d+(\.\d+)?",
    r"space/[a-z][a-z0-9-]*",
    r"radius/[a-z0-9][a-z0-9-]*",
    r"border-width/\d+(\.\d+)?",
    r"font/size/\d+(\.\d+)?",
    r"font/family/[a-z][a-z0-9-]*",
    r"elevation/[a-z0-9][a-z0-9-]*(/[a-z][a-z0-9-]*)?",
    r"motion/duration/\d+",
    r"motion/easing/[a-z][a-z0-9-]*",
]


def check_color_name(name: str) -> list[str]:
    """색 토큰 이름 검사. 위반 메시지 목록(빈 목록 = 통과)."""
    errs: list[str] = []
    parts = name.split("/")
    if parts[0] in MODULES:
        parts = parts[1:]
    if len(parts) != 2:
        return [f"{name}: 형식은 {{property}}/{{tone}}-{{emphasis}}-{{state}} (슬래시는 property 뒤 한 번)"]
    prop, rest = parts
    if prop not in PROPERTIES:
        return [f"{name}: property '{prop}' 미승인 (bg · fg · stroke)"]
    segs = rest.split("-")
    # 순서: tone(0) → layer수식어(1) → emphasis(2) → state(3)
    order = -1
    prev_tone = None
    for s in segs:
        if s in TONES or (s in STROKE_ONLY_TONES):
            rank = 0
            if s in STROKE_ONLY_TONES and prop != "stroke":
                errs.append(f"{name}: '{s}' 는 stroke 전용 tone")
            prev_tone = s
        elif s in LAYER_QUALIFIERS:
            rank = 1
            if prev_tone != "layer" or order != 0:
                errs.append(f"{name}: '{s}' 는 tone 'layer' 바로 뒤에서만 허용")
        elif s in EMPHASES:
            rank = 2
        elif s in STATES:
            rank = 3
        else:
            errs.append(f"{name}: 미승인 어휘 '{s}' (어휘 추가는 별도 안건)")
            continue
        if rank <= order:
            errs.append(f"{name}: 순서 위반 — '{s}' 위치 (tone → emphasis → state)")
        order = rank
    return errs


def check_name(name: str, role: str) -> list[str]:
    """role = primitive | brand | semantic | module | 비색상 컬렉션 role."""
    errs: list[str] = []
    low = name.lower()
    for seg in re.split(r"[/-]", low):
        if seg in COMPONENT_WORDS:
            errs.append(f"{name}: 컴포넌트명 '{seg}' 포함 금지")
    if role == "primitive":
        return errs
    if role == "brand":
        p = name.split("/")
        ok = (len(p) == 3 and p[0] == "brand" and p[1] in BRAND_RAMPS and p[2] in BRAND_STEPS) or \
             re.fullmatch(r"font/family/[a-z][a-z0-9-]*", name)
        if not ok:
            errs.append(f"{name}: Brand 는 brand/(primary|secondary)/{{11단계}} 또는 font/family/{{role}} 만")
        return errs
    if role in ("semantic", "module"):
        if role == "module" and name.split("/")[0] not in MODULES:
            errs.append(f"{name}: Module 토큰은 commerce/ 또는 messenger/ 로 시작")
        if role == "semantic" and name.split("/")[0] in MODULES:
            errs.append(f"{name}: 모듈 접두사는 Module 컬렉션에만")
        return errs + check_color_name(name)
    if not any(re.fullmatch(p, name) for p in NON_COLOR_PATTERNS):
        errs.append(f"{name}: 비색상 문법 위반 (references/naming.md 비색상 표)")
    return errs


# ── 플랫폼 변환 ─────────────────────────────────────────────

def _camel(words: list[str]) -> str:
    out = words[0] + "".join(w[:1].upper() + w[1:] for w in words[1:])
    return "n" + out if out[:1].isdigit() else out


def to_path(name: str) -> list[str]:
    return name.split("/")


def to_css(name: str) -> str:
    return "--" + name.replace("/", "-").replace(".", "-")


def to_code(name: str) -> tuple[str, str]:
    """(group, key) — TS tokens.{group}.{key} · Dart context.tokens.{group}.{key}"""
    parts = name.split("/")
    group = _camel(parts[0].split("-"))
    rest = "-".join(parts[1:]).replace(".", "-").split("-")
    return group, _camel(rest)


if __name__ == "__main__":
    for n in ["bg/neutral-solid", "fg/warning-contrast", "commerce/bg/brand-weak",
              "font/size/14", "spacing/4", "radius/2xl", "motion/duration/200"]:
        print(f"{n:28} {to_css(n):28} {'.'.join(to_code(n))}")
    for n, r in [("bg/layer-default", "semantic"), ("bg/solid-brand", "semantic"),
                 ("bg/button-primary", "semantic"), ("stroke/focus", "semantic"),
                 ("fg/focus", "semantic"), ("bg/info-solid", "semantic"),
                 ("brand/primary/500", "brand"), ("brand/primary", "brand")]:
        print(n, check_name(n, r) or "OK")
