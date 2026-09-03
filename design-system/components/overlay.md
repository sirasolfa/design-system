# Overlays `[F]`

> 출처 — Figma 페이지 **• Overlay** `1595:11129` (섹션 `1600:13981`), Overview 표 `1635:14884`

## Overview 상태표

| 컴포넌트 | Status | Last Update |
|---|---|---|
| Popup | In-progress | N/A |
| Dialog | Done | N/A |
| Drawer | Done | 1/27/26 |
| Bottom sheet | Done | 1/21/26 |
| Toast | Done | 1/27/26 |
| Tooltip | In-progress | N/A |
| Snackbar | Done | 1/27/26 |
| System message | Before | N/A |
| Pulldown menu | Before | N/A |

상세 프레임이 있는 것은 6종(Dialog, Drawer, Bottom Sheet, Toast, Tooltip, Snack Bar)이며,
`Popup` · `System message` · `Pulldown menu` 는 상세 프레임이 없습니다.

---

## Dialog `1049:3492`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Modal` | `viewport=desktop, size=lg \| md \| sm` · `viewport=mobile, size=sm` |
| `Alert` | *(베리언트 없음)* |
| `Overlay` | `type=modal \| alert` |

모바일은 `size=sm` 만 존재합니다.

### 시안에 적힌 규칙 (원문)

> **다이얼로그의 최대 높이는 화면 높이 기준 20% 여백을 가져야 합니다.**

프레임에 `예시-높이 1080` 블록으로 검증 예시가 그려져 있습니다. `Dim` 레이어가 별도로 존재합니다.

## Drawer `1065:18140`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Side Drawer` | `Open drawer on=right`, `Size=default` |

프로퍼티 이름이 문장형(`Open drawer on`)이고 첫 글자가 대문자(`Size`)라 다른 컴포넌트와 표기가 다릅니다.
현재 값이 각각 하나뿐이라 좌측 오픈/다른 사이즈는 미정의입니다.

### 사용 가이드 — `Drawer(Usage)` `1358:8391`

> **Guide** — 드로어(Drawer)의 사용 예시를 안내합니다.

#### Anatomy

프리뷰에 번호 배지로 표시된 4개 부분입니다.

| # | 이름 |
|---|---|
| 1 | Header |
| 2 | Container |
| 3 | Dimmer |
| 4 | Content area |

#### Spec

| 항목 | 값 |
|---|---|
| Container **Width** | **Changeable (Default: 436px)** — 시안에 빨간 주석으로 명시 |
| Dimmer | `color/bg/overlay/mask` = `rgba(0,0,0,0.4)` |
| Header padding | 좌우 `layout.spacing.xs`(16) · 상하 `layout.spacing.2xs`(12) |
| Header 타이틀 | `Subtitle/1` (18 / SemiBold) |
| 프리뷰 화면 | `1024 × 768` 데스크톱 기준 |

> `[?]` Drawer 헤더 안에 **`정리중`** 이라는 이름의 레이어가 있습니다. 작업 중 표시로 보입니다.
> 헤더 우측 아이콘도 `application/settings` + `Icon/Pictogram/ShoppingBag` 으로,
> 드로어 헤더의 표준 액션이 무엇인지 확정되지 않은 상태로 보입니다.

## Bottom Sheet `1065:18681`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `BottomSheet` | `type=default` |
| `Overlay` | `type=bottom` |

### 사용 가이드 — `Action Area(Usage)`

> **Guide** — 액션 영역(Action Area) 컴포넌트의 사용 예시를 안내합니다.

세 컴포넌트를 순서대로 설명합니다.

#### 1. Button Pair
> ActionArea 내부의 버튼 쌍으로, 사이즈와 방향 조합을 제공합니다.

| 섹션 | 뷰포트 칩 | 값 |
|---|---|---|
| **Size (Horizontal)** | Desktop / Mobile | `large` · `medium` · `small` |
| **Size (Vertical)** | Desktop / Mobile | `large` · `medium` · `small` |

가로 배치는 보조 버튼(연한 배경)이 왼쪽, 주 버튼(어두운 배경)이 오른쪽입니다.
세로 배치는 **주 버튼이 위**, 보조 버튼이 아래로 순서가 뒤집힙니다.

#### 2. Button Action Bar
> 아이콘 버튼과 메인 버튼을 결합한 액션 바 형태입니다.

| 섹션 | 뷰포트 칩 | 값 |
|---|---|---|
| **Size** | Desktop / Mobile | `large` · `medium` |
| **Press Heart Button** | Desktop / Mobile | `large` · `medium` |

구성은 `하트(찜) 아이콘 버튼 + 장바구니 아이콘 버튼 + 메인 버튼` 순입니다.
`Press Heart Button` 은 찜을 누른 상태로, **하트만 채워진 빨강**으로 바뀝니다.

#### 3. Action Area
> 버튼 배치 방향에 따라 Horizontal, Vertical 두 가지 레이아웃을 제공합니다.

| 섹션 | 뷰포트 칩 | 값 |
|---|---|---|
| **Direction** | Mobile | `horizontal` · `vertical` |

프리뷰는 장바구니 바텀시트 위에 얹은 상태로 보여줍니다:
`CartItem`, `└ Checkbox-atomic`, `Ratio`, `Price`, `addOptionRow`, `└ OptionRow`, `IconOnly`, `ActionArea`, `ButtonPair`.
→ [../patterns/commerce.md](../patterns/commerce.md)

> `[?]` 이 가이드는 파일 안에 **두 벌** 존재합니다. Bottom Sheet 안의 `3572:31464`(1440×1870)와,
> 페이지 트리에서 조회되지 않는 `3261:4202`(1440×2791). 위 내용은 더 최신으로 보이는 후자 기준입니다.
> 어느 쪽이 정본인지 확인이 필요합니다.

## Toast `1368:9769`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Toast` | `type=success \| error \| info` |
| `Toast/Text` | `Icon=True \| False`, `Line=Single \| Multi` |
| `Toast/Icon` | `Option=Check mark \| Loading \| Exclamation Mark \| Custom` |

### 사용 가이드 — `Toast(Usage)` `1368:10031`

> **Guide** — 토스트(Toast)의 사용 예시를 안내합니다.

`1280 × 5892` 로 이 파일에서 가장 상세한 가이드 중 하나이며, 4개 절로 나뉩니다.

| 절 | 하위 항목 |
|---|---|
| **Element Patterns & Types** | `Postition` ※오타 · `Number of Line` |
| **Behavior** | `Appear and Disappear without Loading` · `Appear and Disappear with Loading` |
| **Usage** | `Consider Attention Level` |
| **Design Spec** | `Placement` (Center / Bottom) · `Resizing` (Icon Toast / Text Toast) |

명시된 규칙:

- **Center** — 센터 배치 옵션을 선택하면 아이콘과 토스트 메시지가 **화면의 정중앙에 항상 표시**됩니다.
- **Bottom** — `BottomNavigation`(홈 · 카테고리 · 좋아요 · 마이) 위에 얹혀 표시됩니다.
- 텍스트 길이 기준 예시 문구: **"Text Toast Single Line 최대 스무 자 입력"**

`Toast Case Icons` / `Toast Case Labels` 대응표와 로딩 표현용 레이어가 함께 있습니다
(`Loading Cirlce` — 오타, `Circle`).

> `[?]` 세 절(`Behavior` · `Usage` · `Design Spec`)의 Description 텍스트 노드는 **비어 있습니다.**
> 절 제목만 있고 설명 문장이 아직 작성되지 않았습니다.

## Tooltip `1600:13434` — 베리언트가 가장 많음

| 컴포넌트 | 프로퍼티 | 조합 수 |
|---|---|---|
| `CompactTooltip` | `size=xs \| sm \| md`, `theme=light \| dark`, `type=default \| bold`, `showTrailingIcon=true \| false` | 24 |
| `Tooltip` | `size=sm \| md`, `direction=top \| bottom \| left \| right`, `align=start \| center \| end`, `theme=light \| dark` | 48 |

- `CompactTooltip` 만 `size=xs` 를 가집니다.
- `Tooltip` 은 꼬리 방향(`direction`) × 정렬(`align`) 12조합을 사이즈·테마와 곱합니다.
- **`theme=light | dark` 를 가진 유일한 컴포넌트 군**입니다(Snack Bar 포함 오버레이 계열 특징).

> Change Log(Input Field) `260202` 의 `showTrailingIn 추가` 와 이름이 유사한 `showTrailingIcon` 을 씁니다.

## Snack Bar `1384:7161`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Snack bar` | `Name=Snack bar` |
| `Snack bar/leading item` | `Type=Icon \| Slot` |

`Link` · `Item` · `Lable`(오타 — `Label`) · `direction/chevron` 아이콘으로 구성됩니다.

## Search(Usage) `1170:5163`

이 페이지에 함께 놓인 `1440 × 9388` 크기의 검색 사용 가이드입니다.
Overview 상 **Inputs > Search (Done)** 항목을 다룹니다.

| 절 | 노드 |
|---|---|
| **State** | `1170:5170` |
| **Spec** | `1170:5195` |
| **Behavior** | `1171:6187` |
| **With Keyboard** | `1171:6777` |

`With Keyboard` 는 모바일 키보드가 올라온 상태의 검색 화면을 따로 다룹니다.
→ [inputs.md](inputs.md) · [../patterns/README.md](../patterns/README.md)

> `[?]` 각 절의 Description 텍스트는 미조사입니다(프리뷰가 커서 절 제목만 확인).

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | `Popup` · `System message` · `Pulldown menu` 상세 프레임 없음 |
| 2 | `Drawer` 의 `Open drawer on` 이 `right` 만, `Size` 가 `default` 만 존재 — 좌측/다른 사이즈 계획 |
| 3 | 프로퍼티 이름 표기 혼용 — `size`(소문자) vs `Size`/`Type`/`Name`(대문자), 문장형 `Open drawer on` |
| 4 | 오타 레이어: `Loading Cirlce`, `Lable` |
| 5 | `theme=light\|dark` 가 Tooltip 계열에만 존재. 다크 테마 정책 전반은 미정의 |
| 6 | Dialog "화면 높이 20% 여백" 규칙이 모바일에도 동일 적용되는지 |
| 7 | 각 컴포넌트의 `Version Info` 본문 미조사 |
| 8 | `Action Area(Usage)` 가 두 벌 존재 (`3572:31464` / `3261:4202`) — 정본 확인 필요 |
| 9 | Toast 가이드의 `Behavior`·`Usage`·`Design Spec` 설명 문장이 비어 있음 |
| 10 | Usage 가이드가 **없는** 오버레이: Dialog · Tooltip · Snack Bar |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
