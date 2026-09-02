# NDS — NOVERA Design System

NOVERA 디자인 시스템의 **문서 저장소**입니다.
Figma 원본에서 토큰·컴포넌트·패턴을 읽어 옮기고, **Figma에 있는 사실과 AI가 제안한 가이드라인을 파일 단위로 분리**해 둡니다.

> 문서만 담습니다. 코드 토큰 패키지나 컴포넌트 라이브러리는 아직 없습니다.
> 만들 때의 방향 제안은 [`ai-guidelines.md`](design-system/guidelines/ai-guidelines.md)에 모아 두었습니다.

**[Figma 원본 열기](https://www.figma.com/design/OJqTwQ8gHDGcvOOkOfYRgM/NDS---NOVERA-Design-System?node-id=0-1)**
· [파운데이션](design-system/foundations/README.md)
· [컴포넌트](design-system/components/README.md)
· [패턴](design-system/patterns/README.md)
· [AI 제안](design-system/guidelines/ai-guidelines.md)

---

## 먼저 읽을 것 — 사실과 제안의 구분

이 저장소는 **두 종류의 내용을 물리적으로 분리**합니다. 표기를 보고 신뢰 수준을 판단하세요.

| 표기 | 뜻 | 위치 |
|---|---|---|
| **`[F]`** | Figma에서 **직접 읽은 값**. 토큰 값, 컴포넌트/베리언트 이름, 시안에 적힌 문구. 노드 ID를 병기합니다. | `foundations/` · `components/` · `patterns/` · `guidelines/naming.md` · `guidelines/changelog.md` |
| **`[?]`** | Figma에 존재하지만 값을 끝까지 읽지 못했거나, **시안 내부에서 값이 서로 어긋나는** 항목. | 위 문서들의 "확인 필요" 절 |
| **`[A]`** | Figma에 근거가 없는, AI가 관례에 기대어 만든 **초안**. 채택 전까지 규범이 아닙니다. | **[`guidelines/ai-guidelines.md`](design-system/guidelines/ai-guidelines.md) 한 곳에만** |

`foundations/`, `components/`, `patterns/` 본문에는 `[A]` 항목을 섞지 않습니다.
제안이 필요한 자리에는 각 문서 끝에 링크만 겁니다.
`[A]` 항목에는 **"근거"**(무엇에 기댔는지)와 **"확정 조건"**(무엇을 확인하면 사실이 되는지)이 함께 붙어 있습니다.

---

## 문서 지도

```
README.md                           ← 지금 이 문서
        ↓
design-system/
├── README.md                       인덱스 · 표기 규약 · 원본 갱신 방법
├── foundations/                    [F] 토큰
│   ├── color.md                    primitive 팔레트 · semantic 토큰
│   ├── typography.md               폰트 · 텍스트 스타일 29종
│   ├── layout.md                   gap · spacing · grid · breakpoint
│   ├── shape.md                    rounded · border-width
│   ├── elevation.md                shadow 4단계
│   ├── iconography.md              아이콘 그리드 · 사이즈 · 네이밍 · 목록
│   └── brand.md                    로고 · 파비콘 · OG 이미지
├── components/                     [F] 인벤토리 50종 + 베리언트
│   ├── content-display.md          Card · Avatar · Price · Table · List …
│   ├── overlay.md                  Dialog · Drawer · BottomSheet · Toast · Tooltip …
│   ├── inputs.md                   Text input · Checkbox · Search …
│   ├── button.md
│   ├── navigation.md
│   └── indicator-status.md
├── patterns/                       [F] Figma "(Usage)" 프레임 = 조합 패턴
│   └── commerce.md                 상품 카드 · 상품 상세 · 장바구니 · 이벤트
└── guidelines/
    ├── naming.md                   [F] 네이밍 규칙 (Change Log 원문)
    ├── changelog.md                [F] Change Log 전문
    └── ai-guidelines.md            [A] AI 제안 — 이 파일만 제안입니다
```

---

## 파운데이션 한눈에 `[F]`

| 축 | 값 |
|---|---|
| 폰트 | `Pretendard Variable` — Regular 400 / SemiBold 600 / Bold 700 |
| 텍스트 스타일 | Display 2 · Title 5 · Subtitle 3 · Body 4 · Action 3(+underline 3) · Label 3 · Caption 3(+semibold 3) |
| 색 (primitive) | gray 12단계 + pink·red·yellow·green·cyan·blue·indigo 각 11단계 + base 2 + alpha black/white 각 6 |
| 색 (semantic) | `text` 6 · `border` 5 · `divider` 4 · `bg` 6 · `icon` 6 |
| 브랜드 | `brand/default` `#4f7cff` (= `color/blue/600`) |
| 간격 | `layout.gap.*` (px 이름) 15단계 / `layout.spacing.*` (3xs~3xl) 8단계 |
| 라운드 | `none 0 · xxs 4 · xs 6 · sm 8 · md 12 · lg 16 · xl 24 · full 999` |
| 보더 | `1px` / `2px` |
| 그림자 | `subtle · default · raised · overlay` |
| 아이콘 | 24×24 기준 그리드, 사이즈 `12·16·20·24·28·32·40` |
| 브레이크포인트 | Desktop `1440×960` (≥1200) · Tablet `768×960` (768–1199) · Mobile `375×812` |

→ [`foundations/`](design-system/foundations/README.md)

## 컴포넌트 현황 `[F]`

Figma Overview 페이지(`1183:7436`)에 적힌 상태 그대로입니다.

| 카테고리 | Done | In-progress | Before | 계 |
|---|---|---|---|---|
| [Navigation](design-system/components/navigation.md) | 5 | 2 | 2 | 9 |
| [Button](design-system/components/button.md) | 0 | 1 | 1 | 2 |
| [Content display](design-system/components/content-display.md) | 2 | 2 | 5 | 9 |
| [Indicator & Status](design-system/components/indicator-status.md) | 2 | 0 | 6 | 8 |
| [Inputs](design-system/components/inputs.md) | 3 | 2 | 8 | 13 |
| [Overlays](design-system/components/overlay.md) | 5 | 2 | 2 | 9 |
| **합계** | **17** | **9** | **24** | **50** |

---

## 코드로 옮기기 전 확인할 불일치 `[F]` `[?]`

문서를 그대로 구현하면 어긋나는 지점입니다. 사람이 정본을 정해야 합니다.

| # | 항목 | 상태 |
|---|---|---|
| 1 | **`layout.spacing` 상위 3단계** | 인쇄된 라벨은 `xl 32 / 2xl 40 / 3xl 48`, 변수 실제값과 시안 막대는 **`28 / 32 / 40`** → [layout.md](design-system/foundations/layout.md) |
| 2 | **`color.border.strong` / `.disabled`** | 표의 매핑(`gray/300` / `gray/400`)과 변수값(gray/400 / gray/300)이 **서로 뒤바뀜** → [color.md](design-system/foundations/color.md) |
| 3 | **gray 리넘버링 잔여** | Change Log `251224`의 `gray 50→100, 100→150` 이후 `bg.subtle`·`bg.muted`·`divider.soft`·`text.primary` 라벨이 옛 번호 → [color.md](design-system/foundations/color.md) |
| 4 | **오타 토큰** | `color.text.priamry`, `color.divider.defualt`, `sementic/background/*`, Price의 `discout` → [naming.md](design-system/guidelines/naming.md) |

## 조사되지 않은 영역

추정으로 채우지 않고 비워 둔 것들입니다.

- **Grid의 컬럼 / 거터 / 마진** — Figma layout grid 속성이라 MCP 어느 경로로도 노출되지 않습니다.
  확정된 것은 뷰포트 크기(1440 / 768 / 375)와 전환 기준뿐입니다.
- **Navigation · Button · Inputs · Indicator & Status 의 상세 시안** — Figma 파일에 페이지가 4개뿐이라
  이 카테고리들은 상세 프레임이 없습니다. 해당 문서는 Overview 상태표와 Change Log 기반입니다.
- `Caption/1`, `Caption/3`, `Caption/semibold/2·3` 의 사이즈/행간
- `color.icon.*` 의 실제 HEX

---

## 원본과 갱신

| | |
|---|---|
| Figma 파일 | [NDS - NOVERA Design System](https://www.figma.com/design/OJqTwQ8gHDGcvOOkOfYRgM/NDS---NOVERA-Design-System?node-id=0-1) |
| File key | `OJqTwQ8gHDGcvOOkOfYRgM` |
| 라이브러리명 | `NDS - NOVERA Design System` |
| 변수 컬렉션 | `primitive` (예: `number/unit/*`, `color/*`) |
| Figma 페이지 | Overview `1183:7436` · Foundation `0:1` · • Content Display `1595:11126` · • Overlay `1595:11129` |
| 조사 방법 | Figma MCP — `get_metadata` / `get_variable_defs` / `get_screenshot` / `search_design_system` |
| 최초 조사일 | 2026-09-02 |
| 적용 서비스 | [`sirasolfa/shop-lab`](https://github.com/sirasolfa/shop-lab) — NOVERA shop |

갱신 절차와 MCP 호출 순서는 [`design-system/README.md`](design-system/README.md#원본-갱신-방법)에 있습니다.
Figma Change Log에 항목이 추가되면 [`changelog.md`](design-system/guidelines/changelog.md)에 옮기고 영향 문서를 함께 고칩니다.
`[?]` 가 해소되면 사실 문서로 옮기고 표기를 지웁니다.
