#!/usr/bin/env python3
"""claude.ai '디자인 시스템'(Design System 아티팩트)에 올릴 파일 묶음을 만든다.

입력  design-system/  (사실 문서 [F]/[?])
출력  claude-ai/project/

- tokens.json      foundations/*.md 의 [F] 값을 Design System 타입의 토큰 형식으로 옮김
- 섹션 *.md         foundations · 컴포넌트 인벤토리 · patterns · naming · changelog
- components/<Comp>/README.md   카테고리별 컴포넌트 문서
- design-system.json            인덱스 (--index 옵션일 때만, 게시 직전에 생성)

[A] 문서(guidelines/ai-guidelines.md)와 요청 목록(guidelines/design-requests.md)은 넣지 않는다.
README.md 와 components/Cover/preview.html 은 손으로 쓴 파일이라 이 스크립트가 건드리지 않는다.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "design-system"
OUT = ROOT / "claude-ai" / "project"

# 섹션: 출력 경로 ← 원본 경로. 경로 순서가 곧 화면의 섹션 순서다.
SECTIONS = {
    "01-foundations/00-overview.md": "foundations/README.md",
    "01-foundations/01-color.md": "foundations/color.md",
    "01-foundations/02-typography.md": "foundations/typography.md",
    "01-foundations/03-layout.md": "foundations/layout.md",
    "01-foundations/04-shape.md": "foundations/shape.md",
    "01-foundations/05-elevation.md": "foundations/elevation.md",
    "01-foundations/06-iconography.md": "foundations/iconography.md",
    "01-foundations/07-brand.md": "foundations/brand.md",
    "02-components.md": "components/README.md",
    "03-patterns/00-overview.md": "patterns/README.md",
    "03-patterns/01-commerce.md": "patterns/commerce.md",
    "04-guidelines/01-naming.md": "guidelines/naming.md",
    "04-guidelines/02-changelog.md": "guidelines/changelog.md",
}

# 컴포넌트 카테고리: 폴더 이름(ASCII 식별자) ← 원본, 첫 문장(요약)
COMPONENTS = {
    "Button": ("components/button.md", "Button 카테고리의 Overview 상태표와 Change Log에 적힌 사실입니다."),
    "Inputs": ("components/inputs.md", "Inputs 카테고리(입력 필드·선택 컨트롤)의 Overview 상태표와 Change Log에 적힌 사실입니다."),
    "Navigation": ("components/navigation.md", "Navigation 카테고리의 Overview 상태표입니다."),
    "ContentDisplay": ("components/content-display.md", "Content Display 페이지의 컴포넌트 세트·베리언트·Usage 가이드입니다."),
    "Overlay": ("components/overlay.md", "Overlay 페이지(Dialog·Drawer·Bottom Sheet·Toast 등)의 컴포넌트 세트·베리언트·Usage 가이드입니다."),
    "IndicatorStatus": ("components/indicator-status.md", "Indicator & Status 카테고리의 Overview 상태표입니다."),
}

LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def clean(md: str) -> str:
    """[A] 문서로 가는 줄을 빼고, 저장소 안 상대 링크는 텍스트만 남긴다(아티팩트에선 깨지므로)."""
    lines = [l for l in md.splitlines() if "ai-guidelines" not in l]
    text = "\n".join(lines).rstrip()
    # 끝에 남은 구분선 정리
    text = re.sub(r"(\n---\s*)+$", "", text).rstrip() + "\n"

    def repl(m):
        label, target = m.group(1), m.group(2)
        if target.startswith(("http://", "https://")):
            return m.group(0)
        if target.startswith("#"):  # 같은 문서 앵커는 유지
            return m.group(0)
        return label

    return LINK.sub(repl, text)


# ---------- tokens ----------

GRAY = {"50": "#fcfdff", "100": "#f9fafd", "150": "#f4f6fb", "200": "#edf0f5", "300": "#e3e6ee",
        "400": "#c5c9d3", "500": "#a6acb7", "600": "#888e9c", "700": "#697180", "800": "#4b5465",
        "900": "#2f3744", "950": "#171c24"}
STEPS = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"]
HUES = {
    "pink": ["#fef5fc", "#fde6f7", "#fbccef", "#f8ade5", "#f58ada", "#f159cb", "#e900af", "#c60095", "#a3007a", "#800060", "#5d0046"],
    "red": ["#fff7f8", "#ffeef1", "#ffc5cd", "#ffa2af", "#ff7a8c", "#f9556e", "#e6374f", "#c8263d", "#9e1d31", "#751524", "#4d0d18"],
    "yellow": ["#fffdf7", "#fffaee", "#ffedb8", "#ffe291", "#ffd363", "#ffc439", "#ffb020", "#cc8a18", "#996713", "#66430c", "#3d2707"],
    "green": ["#f7fcf9", "#f1fcf4", "#c0eed0", "#96e1b4", "#68d093", "#3fbe75", "#1fa45c", "#17824a", "#10613a", "#0a3f27", "#051f15"],
    "cyan": ["#f5fdff", "#ebfcff", "#b3f2ff", "#80eaff", "#3ddfff", "#00d4ff", "#00b3d6", "#008ca8", "#00667a", "#004452", "#00262e"],
    "blue": ["#f9fbff", "#eef3ff", "#cedbff", "#aec3ff", "#8facff", "#6f94ff", "#4f7cff", "#355fea", "#2747be", "#1a318b", "#111f5c"],
    "indigo": ["#f5f3ff", "#e4e4ff", "#cacdff", "#a8b0ff", "#8a93ff", "#6c73ff", "#524fe2", "#3c37c2", "#330099", "#260070", "#19004a"],
}
ALPHA = {"8": "14", "16": "29", "24": "3d", "40": "66", "64": "a3", "80": "cc"}

PRIM_NOTE = "Primitive. Figma `{path}`. 화면·컴포넌트에 직접 쓰지 않고 semantic 토큰을 통해 쓴다."


def tok(name, value, usage):
    return {"name": name, "value": value, "usage": usage}


def color_tokens():
    t = []
    # semantic 먼저 (변수 실제값 기준, primitive 별칭)
    S = [
        ("color-text-primary", "{color-gray-950}", "`color/text/primary` — 페이지/섹션 제목, 가장 중요한 텍스트. 변수 실제값 = gray/950 (문서 표 라벨은 gray/900, 리넘버링 전 번호) [?]"),
        ("color-text-secondary", "{color-gray-800}", "`color/text/secondary` — 일반 본문 텍스트 기본 값."),
        ("color-text-tertiary", "{color-gray-600}", "`color/text/tertiary` — 보조 설명, 서브 타이틀, 메타 정보(시간, 서브 라벨 등)."),
        ("color-text-muted", "{color-gray-500}", "`color/text/muted` — 플레이스홀더, 덜 중요한 설명 텍스트(캡션)."),
        ("color-text-disabled", "{color-gray-400}", "`color/text/disabled` — 비활성 상태 텍스트."),
        ("color-text-inverse", "{color-base-white}", "`color/text/inverse` — 어두운 배경 위 반전 텍스트."),
        ("color-text-status-link", "{color-blue-700}", "`color/text/status/link` — 링크 텍스트 (표기 `color.text.link`)."),
        ("color-text-status-negative", "{color-red-600}", "`color/text/status/negative` — 할인율, Label 필수 표시(*). Semantic 표에는 없음 [?]"),
        ("color-text-brand", "{color-blue-600}", "`color/text/brand` — 브랜드 텍스트. Semantic 표에는 없고 변수로만 존재."),
        ("color-text-subtle", "#464c53", "`color/text/subtle` — Dialog(Usage) 설명 문장. gray 팔레트 어느 단계와도 일치하지 않음 [?]"),
        ("color-border-default", "{color-gray-200}", "`color/border/default` — 카드, 인풋, 컨테이너 등 대부분 요소의 기본 테두리."),
        ("color-border-strong", "{color-gray-400}", "`color/border/strong` — 섹션 구분, 선택·포커스 블록 등 더 진한 테두리. 변수값(gray/400)과 문서 표(gray/300)가 disabled와 뒤바뀜 [?]"),
        ("color-border-disabled", "{color-gray-300}", "`color/border/disabled` — 비활성 테두리. 변수값(gray/300)과 문서 표(gray/400)가 strong과 뒤바뀜 [?]"),
        ("color-border-neutral", "{color-gray-300}", "`color/border/neutral` — Semantic 표에는 없고 변수로만 존재."),
        ("color-border-inverse", "{color-base-white}", "`color/border/inverse` — 어두운 배경, 브랜드 컬러 위 반전 테두리."),
        ("color-border-thumbnail", "{color-alpha-black8}", "`color/border/thumbnail` — 썸네일 테두리 (표에 설명 없음)."),
        ("color-divider-soft", "{color-gray-150}", "`color/divider/soft` — 표 라벨은 gray/100, 변수 실제값은 gray/150 [?]"),
        ("color-divider-default", "{color-gray-200}", "`color/divider/default` — 기본 디바이더. Figma 표 표기는 오타 `color.divider.defualt` [?]"),
        ("color-divider-strong", "{color-gray-300}", "`color/divider/strong` — 섹션 경계, 카드 그룹 사이 등 구획을 명확히 나누는 진한 디바이더."),
        ("color-divider-inverse", "{color-base-white}", "`color/divider/inverse` — surface.inverse, brand 영역 위 반전 디바이더."),
        ("color-bg-surface-default", "{color-base-white}", "`color/bg/surface/default` (표기 `color.bg.default`) — 기본 배경."),
        ("color-bg-surface-subtle", "{color-gray-100}", "`color/bg/surface/subtle` — 섹션을 살짝 분리하거나 카드/레이아웃 뒤에 까는 보조 배경. 표 라벨은 gray/50 [?]"),
        ("color-bg-surface-muted", "{color-gray-150}", "`color/bg/surface/muted` — 표 라벨은 gray/100, 변수 실제값은 gray/150 [?]"),
        ("color-bg-surface-disabled", "{color-gray-200}", "`color/bg/surface/disabled` — 비활성 배경."),
        ("color-bg-surface-neutral-soft", "{color-gray-150}", "`color/bg/surface/neutral-soft` — Dialog 보조 버튼(취소) 배경. Semantic 표에는 없음 [?]"),
        ("color-bg-surface-inverse", "{color-gray-900}", "`color/bg/surface/inverse` — Dialog 주 버튼(확인) 배경. Semantic 표에는 없음 [?]"),
        ("color-bg-inverse", "{color-gray-900}", "`color/bg/inverse` — 반전 배경."),
        ("color-bg-overlay-dim", "{color-alpha-black64}", "`color/bg/overlay/dim` (표기 `color.bg.dim`) — 64% 딤."),
        ("color-bg-overlay-mask", "{color-alpha-black40}", "`color/bg/overlay/mask` — 40% 딤. Drawer Dimmer. Semantic 표에 누락, dim과의 구분 기준 미확인 [?]"),
        ("color-icon-primary", "{color-gray-800}", "`color.icon.primary` — 기본 아이콘 색(주요 기능, 네비게이션, 리스트 정보 아이콘). 매핑은 표 기준, 변수 실제값 미확인 [?]"),
        ("color-icon-secondary", "{color-gray-600}", "`color.icon.secondary` — 서브 액션, 보조 정보 아이콘. 매핑은 표 기준 [?]"),
        ("color-icon-muted", "{color-gray-500}", "`color.icon.muted` — 설명용·메타 정보 아이콘. 매핑은 표 기준 [?]"),
        ("color-icon-disabled", "{color-gray-400}", "`color.icon.disabled` — 클릭/탭 불가 비활성 아이콘. 매핑은 표 기준 [?]"),
        ("color-icon-primary-bg", "{color-gray-100}", "`color.icon.primary-bg` — 표에 설명 없음. 매핑은 표 기준 [?]"),
        ("color-icon-inverse", "{color-base-white}", "`color.icon.inverse` — 표에 설명 없음. 매핑은 표 기준 [?]"),
        ("color-icon-status-primary", "{color-blue-600}", "`color/icon/status/primary` — 변수로만 존재."),
        ("color-icon-brand-bg", "{color-blue-100}", "`color/icon/brand-bg` — 변수로만 존재."),
        ("brand-default", "{color-blue-600}", "`brand/default` — 브랜드 기본색. brand 스케일은 default·strongest 두 단계만 확인 [?]"),
        ("brand-strongest", "{color-blue-900}", "`brand/strongest` — 브랜드 가장 진한 색."),
    ]
    t += [tok(*s) for s in S]
    for k, v in GRAY.items():
        t.append(tok(f"color-gray-{k}", v, PRIM_NOTE.format(path=f"color/gray/{k}")))
    for hue, vals in HUES.items():
        for s, v in zip(STEPS, vals):
            t.append(tok(f"color-{hue}-{s}", v, PRIM_NOTE.format(path=f"color/{hue}/{s}")))
    t.append(tok("color-base-black", "#000000", PRIM_NOTE.format(path="color/base/black")))
    t.append(tok("color-base-white", "#ffffff", PRIM_NOTE.format(path="color/base/white")))
    for n, hx in ALPHA.items():
        t.append(tok(f"color-alpha-black{n}", f"#000000{hx}", PRIM_NOTE.format(path=f"color/alpha/black{n}") + f" 불투명도 {n}%."))
    for n, hx in ALPHA.items():
        t.append(tok(f"color-alpha-white{n}", f"#ffffff{hx}", PRIM_NOTE.format(path=f"color/alpha/white{n}") + f" 불투명도 {n}%."))
    return t


def style(name, size, weight, lh, ls, usage):
    return {"name": name, "fontSize": f"{size}px", "fontWeight": weight, "lineHeight": lh,
            "letterSpacing": f"{ls}px", "usage": usage}


def type_tokens():
    g = []
    g.append({"name": "Display", "family": "sans", "styles": [
        style("Display-1", 56, 700, 1.2, -1, "Figma 텍스트 스타일 `Display/1`. 폰트 변수 `typo/font-family/primary` 참조."),
        style("Display-2", 44, 700, 1.2, -1, "`Display/2`."),
    ]})
    g.append({"name": "Title", "family": "sans", "styles": [
        style(f"Title-{i}", s, 700, 1.3, 0, f"`Title/{i}`. 위계 T1>T2>…(Change Log 251217에서 Title·Heading 통합).")
        for i, s in zip(range(1, 6), [40, 32, 26, 22, 20])]})
    g.append({"name": "Subtitle", "family": "sans", "styles": [
        style("Subtitle-1", 18, 600, 1.4, 0, "`Subtitle/1`."),
        style("Subtitle-2", 16, 600, 1.4, 0, "`Subtitle/2`."),
        style("Subtitle-3", 14, 600, 1.4, 1, "`Subtitle/3`."),
    ]})
    g.append({"name": "Body", "family": "sans", "styles": [
        style(f"Body-{i}", s, 400, 1.4, 0, f"`Body/{i}`. Body는 기본값으로 사용한다(Typography(Usage) 원문).")
        for i, s in zip(range(1, 5), [18, 16, 14, 13])]})
    g.append({"name": "Action", "family": "sans", "styles": [
        style("Action-1", 16, 600, 1.5, 0, "`Action/1` — 버튼에 쓰는 텍스트."),
        style("Action-2", 14, 600, 1.5, 1, "`Action/2`."),
        style("Action-3", 12, 600, 1.5, 1, "`Action/3`."),
        style("Action-underline-1", 16, 600, 1.5, 0, "`Action/underline/1` — Action/1과 같고 밑줄 장식만 다르다."),
        style("Action-underline-2", 14, 600, 1.5, 1, "`Action/underline/2` — 밑줄."),
        style("Action-underline-3", 12, 600, 1.5, 1, "`Action/underline/3` — 밑줄."),
    ]})
    g.append({"name": "Label", "family": "sans", "styles": [
        style("Label-1", 16, 600, 1.5, 0, "`Label/1`."),
        style("Label-2", 14, 600, 1.4, 1, "`Label/2`."),
        style("Label-3", 13, 600, 1.4, 1, "`Label/3`."),
        style("Label-4", 12, 600, 1.4, 1, "`Label/4` — Label(Usage)·OptionRow(Usage) 레이블."),
    ]})
    g.append({"name": "Caption", "family": "sans", "styles": [
        style("Caption-2", 11, 400, 1.4, 1, "`Caption/2` — 보조 설명, 부가 정보, 상태 안내 등 가장 작은 텍스트. (`Caption/1`·`Caption/3` 값은 미확인 [?])"),
        style("Caption-semibold-1", 12, 600, 1.4, 1, "`Caption/semibold/1`. (`Caption/semibold/2` 값은 미확인 [?])"),
        style("Caption-semibold-3", 10, 600, 1.5, 1, "`Caption/semibold/3` — Price 컴포넌트의 통화 코드(KRW)."),
    ]})
    g.append({"name": "Price", "family": "sans", "styles": [
        style("Price-1", 12, 400, 1.4, 0, "`Price/1` — OptionRow(Usage) 할인 전 가격(취소선). 다른 단계 존재 여부 미확인 [?]"),
    ]})
    return {
        "fonts": [],
        "families": {"sans": "\"Pretendard Variable\", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif"},
        "groups": g,
    }


def spacing_tokens():
    t = []
    for v in [0, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 72, 80]:
        t.append(tok(f"layout-gap-{v}", f"{v}px", f"`layout/gap/{v}` — 요소와 요소 사이 거리(카드 리스트, 폼 필드 그룹, 섹션 간 간격)에만 쓴다. 이름 = px 값."))
    SP = [
        ("6xs", 2, "Layout 페이지에 문서화되지 않음(컴포넌트 참조에서 확인) [?]"),
        ("5xs", 4, "Layout 페이지에 문서화되지 않음 [?]"),
        ("4xs", 6, "Layout 페이지에 문서화되지 않음 [?]"),
        ("3xs", 8, ""), ("2xs", 12, ""), ("xs", 16, ""), ("md", 20, ""), ("lg", 24, ""),
        ("xl", 28, "변수값 28. 시안에 인쇄된 라벨은 32px [?]"),
        ("2xl", 32, "변수값 32. 시안에 인쇄된 라벨은 40px [?]"),
        ("3xl", 40, "변수값 40. 시안에 인쇄된 라벨은 48px [?]"),
        ("4xl", 48, "Layout 페이지에 문서화되지 않음(Usage 가이드 패딩에서 확인) [?]"),
        ("5xl", 64, "Layout 페이지에 문서화되지 않음 [?]"),
    ]
    for n, v, note in SP:
        u = f"`layout.spacing.{n}` — 컴포넌트 내부/외부 여백(버튼 padding, 카드 내부 여백, 섹션 상하 여백). `sm` 단계는 없다."
        t.append(tok(f"layout-spacing-{n}", f"{v}px", (u + " " + note).strip()))
    return t


def radius_tokens():
    R = [
        ("none", "0px", "직각 요소 — 리스트 헤더, 디바이더, 테이블 셀."),
        ("xxs", "4px", "소형 UI의 최소 둥글기 — 토글 핸들, 작은 배지, 라벨형 버튼."),
        ("xs", "6px", "Role 설명 비어 있음(260106에 새로 끼운 단계) [?]"),
        ("sm", "8px", "가장 많이 쓰는 기본 둥글기 — 기본 버튼, 입력 필드, 카드."),
        ("md", "12px", "면적이 크거나 강조가 필요한 컴포넌트 — 대형 카드, 강조 섹션, 주요 surface."),
        ("lg", "16px", "떠 있는 레이어 — 다이얼로그, 팝업."),
        ("xl", "24px", "화면 가장자리에서 진입하는 레이어 — 모바일 바텀시트, 드로워."),
        ("full", "999px", "원형·캡슐 — 아바타, 아이콘 버튼, 칩/태그, 숫자 배지."),
    ]
    return [tok(f"shape-rounded-{n}", v, f"`shape.rounded.{n}` — {u}") for n, v, u in R]


def shadow_tokens():
    c12, c08 = "rgba(23, 28, 36, 0.12)", "rgba(23, 28, 36, 0.08)"
    S = [
        ("subtle", f"0 1px 2px 0 {c12}, 0 0 1px 0 {c08}", "배경과 요소를 최소한으로 분리 — 리스트 아이템, 섹션 컨테이너, 헤더·툴바."),
        ("default", f"0 2px 8px 0 {c12}, 0 1px 4px 0 {c08}, 0 0 1px 0 {c08}", "가장 많이 쓰는 기본 깊이 — card, input field, button 기본 상태."),
        ("raised", f"0 6px 12px 0 {c12}, 0 4px 8px 0 {c08}, 0 0 4px 0 {c08}", "인터랙션에 따른 떠오름 — hover, focus, drag. 기본 상태에 상시 적용은 지양."),
        ("overlay", f"0 6px 12px 0 {c12}, 0 4px 8px 0 {c08}, 0 0 24px 0 {c12}", "최상위 레이어 — 모달, 팝오버, 드롭다운, 바텀시트. 일반 버튼·리스트에는 쓰지 않음."),
    ]
    return [tok(f"elevation-shadow-{n}", v, f"`Elevation.shadow.{n}` / Figma 스타일 `Semantic/Shadow/{n.capitalize()}` — {u}") for n, v, u in S]


def tokens():
    return {
        "name": "NOVERA Design System",
        "version": 1,
        "meta": {"source": "Figma OJqTwQ8gHDGcvOOkOfYRgM via sirasolfa/design-system design-system/foundations"},
        "color": {
            "note": "라이트 테마만 정의돼 있다(다크 모드 시안 없음). semantic 토큰은 Figma 변수 실제값 기준이며 primitive 별칭으로 적었다.",
            "themes": [{"id": "light", "name": "Light"}],
            "tokens": color_tokens(),
        },
        "type": type_tokens(),
        "spacing": {"note": "layout/gap/* 은 요소 사이, layout.spacing.* 은 안팎 여백. 임의 숫자를 쓰지 않는다.", "tokens": spacing_tokens()},
        "radius": {"tokens": radius_tokens()},
        "shadow": {"tokens": shadow_tokens()},
        "borderWidth": {"tokens": [
            tok("shape-border-width-1", "1px", "`shape.border-width.1` — 시스템 기본 보더 두께. 입력필드, 버튼, 카드 등 대부분."),
            tok("shape-border-width-2", "2px", "`shape.border-width.2` — 선택된 카드·탭 같은 활성 상태, 윤곽 강조에만."),
        ]},
        "breakpoint": {"note": "Grid 프레임 380:1802 의 적용 기준. 컬럼·거터·마진은 MCP로 읽히지 않아 비워 둔다 [?]. 376–767px 구간 정의 없음 [?].", "tokens": [
            tok("breakpoint-desktop", "1200px", "Desktop — 1200px 이상 (프레임 1440×960)."),
            tok("breakpoint-tablet", "768px", "Tablet — 1200px 미만 768px 이상 (프레임 768×960)."),
            tok("breakpoint-mobile", "375px", "Mobile — 375px 이하 (프레임 375×812)."),
        ]},
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tokens.json").write_text(json.dumps(tokens(), ensure_ascii=False, indent=2) + "\n")
    for dst, src in SECTIONS.items():
        p = OUT / dst
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(clean((SRC / src).read_text()))
    for comp, (src, summary) in COMPONENTS.items():
        md = clean((SRC / src).read_text())
        head, _, rest = md.partition("\n")
        p = OUT / "components" / comp / "README.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"{head}\n\n{summary}\n{rest}")
    if "--index" in sys.argv:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        index = {
            "v": 3, "layout": "files",
            "createdOnFiles": {"v": 1, "at": now},
            "title": "NOVERA Design System",
            "namespace": "NDS",
            "libraries": [],
            "sections": {}, "groups": [], "assetGroups": {}, "blobs": {},
            "docs": {"sections": []},
            "lastChange": {"by": "sirasolfa", "at": now, "via": "Claude Code", "note": "NDS 문서 저장소(sirasolfa/design-system)에서 최초 등록"},
        }
        (OUT / "design-system.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    n = sum(1 for _ in OUT.rglob("*") if _.is_file())
    print(f"wrote {n} files under {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
