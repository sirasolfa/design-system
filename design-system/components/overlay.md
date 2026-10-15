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

### 사용 가이드 — `Dialog(Usage)` `4805:36820`

> **Guide** — 다이얼로그(Dialog)의 사용 예시를 안내합니다.

한 개 절(`height`)로 이뤄집니다.

> 다이얼로그의 최대 높이는 화면 높이 기준 20% 여백을 가져야 합니다.

`예시-높이 1080` 프레임에 측정선과 두 주석이 그려져 있습니다.

| 주석 | 내용 |
|---|---|
| 초록(`color/green/400`) | **Dialog 최대 높이 : 디바이스 화면 높이 기준 20% 여백** |
| 파랑(`color/blue/400`) | **기준 화면 높이 : 1080px** |

프리뷰 Alert 실측값:

| 항목 | 값 |
|---|---|
| 최대 높이 | `864px` (= 1080 × 0.8) |
| 최대 폭 / 폭 | `480px` |
| 패딩 | `layout.spacing.md` (20) |
| 내부 gap | `layout.gap.24` |
| 라운드 | `shape.rounded.md` (12) |
| 그림자 | `semantic/shadow/overlay` |
| Dim | `color/bg/overlay/dim` = `rgba(0,0,0,0.64)` |
| 액션 | `ButtonPair` — 취소(`color/bg/surface/neutral-soft`) / 확인(`color/bg/surface/inverse`), 높이 44 |

`ButtonPair` Figma 컴포넌트 설명(`436:5863`):
> 주요 액션과 보조 액션을 함께 제공하는 버튼 쌍 컴포넌트입니다. 수평/수직 방향과 3가지 사이즈(lg, md, sm)를
> 지원하며, **`showSubButton` 속성으로 보조 버튼의 표시 여부**를 제어할 수 있습니다.

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

> **이 컴포넌트에는 가이드가 두 개 있습니다.** 아래 `Sheet(Usage)` 외에,
> 페이지 최상위의 `BottomSheet(Usage)` 가 시트 자체의 상태·동작을 다룹니다.
> → [아래 절 참조](#bottomsheetusage-11705163--bottom-sheet-두-번째-가이드-f)

### 사용 가이드 — `Sheet(Usage)` `3572:31464` (이전 이름 `Action Area(Usage)`)

> **Guide** — 액션 영역(Action Area)과 바텀시트 높이 규칙의 사용 예시를 안내합니다.

#### 현재 내용은 **Height 규칙 하나뿐**입니다 `[F]`

프레임이 개명되면서 **내용이 교체**됐습니다. 현재 `Content`(`3572:31468`) 안에는
`Height` 절 하나만 있고, 아래 §Button Pair ~ §Action Area 는 **더 이상 이 프레임에 없습니다**.

> **Height** — 최소 높이는 **200px**, 최대 높이는 현재 사용 가능한 **화면 높이의 80%** 입니다.
> 모달과 동일하게 상단 20%를 남기며, 기본 높이는 콘텐츠에 맞춰 자동으로 증가합니다.

프리뷰는 812px 화면 기준 두 가지를 나란히 보여줍니다.

| 프리뷰 | 내용 |
|---|---|
| **최소 200px** | 시트 영역 200px 안에 `핸들` / `본문` / `액션 영역 + 하단 Safe Area`. 위쪽에 "콘텐츠에 맞춰 높이 조정" |
| **최대 80% · 649.6px** | 812 × 0.8 = 649.6px |

##### 세부 규칙 — **TBD(투명도 50%)** `[?]`

같은 절의 불릿 목록은 **`opacity: 0.5`** 로 흐리게 처리돼 있습니다. 확정 전 초안으로 보입니다.

> - 높이 범위: 핸들 최상단부터 화면 하단까지. 핸들·본문·액션 영역·하단 Safe Area를 포함하며 Dim 전체 높이와 구분합니다.
> - 필수 영역과 콘텐츠 한 행이 200px보다 크면 필요한 높이까지 늘리되, 최대 높이를 넘지 않습니다. 최대 높이를 넘는 콘텐츠는 본문만 세로 스크롤하고 핸들과 액션 영역은 고정합니다.
> - 키보드가 열리면 현재 가시 화면 높이를 기준으로 최대 높이를 다시 계산합니다. Safe Area는 중복 합산하지 않습니다.
> - 화면이 짧아 80%가 200px보다 작으면 최대 높이를 우선합니다. 필수 영역도 담기 어렵다면 별도 전체 화면 UI를 사용합니다.
> - 812px 화면 예시: 최소 200px / 최대 649.6px(약 650px).

> **Dialog 와 같은 80% 규칙**입니다. 앞서 "Bottom Sheet 90% vs Dialog 80%" 로 적었던 것은
> 이 Height 절이 생기기 전 `BottomSheet(Usage)` 의 `Max Height 90%` 표기를 따른 것이었습니다.
> 두 수치가 파일 안에 공존합니다. → [아래 확인 필요](#확인-필요)

---

#### 아래 내용은 **이전 버전**(`3261:4202`, 현재 조회 불가) 기록입니다 `[?]`

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

> `[?]` Button Pair · Button Action Bar · Action Area 세 절이 **현재 프레임에서 사라졌습니다.**
> 다른 곳으로 옮겨졌는지, 삭제된 것인지 확인이 필요합니다.
> 다만 `Sheet(Usage)` 의 **부제는 여전히 "액션 영역(Action Area)과…"** 라고 적혀 있어,
> 부제가 내용보다 앞서 있거나 내용이 아직 덜 옮겨진 상태로 보입니다.

## Toast `1368:9769`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Toast` | `type=success \| error \| info` |
| `Toast/Text` | `Icon=True \| False`, `Line=Single \| Multi` |
| `Toast/Icon` | `Option=Check mark \| Loading \| Exclamation Mark \| Custom` |

### 사용 가이드 — `Toast(Usage)` `4493:25180` `[F]`

> **Guide** — 토스트(Toast)의 사용 예시를 안내합니다.

`1440 × 5193`. **이 파일에서 가장 구체적인 가이드**로, 구현에 필요한 수치가 대부분 적혀 있습니다.
2026-10-15 에 전면 재작성됐습니다(이전 `1368:10031` 의 `Element Patterns & Types` 구성은 폐기).

#### 1. Overview

> 토스트(Toast)는 화면 **하단**에 잠시 나타났다가 자동으로 사라지는 피드백 UI입니다.
> 사용자의 작업 흐름을 방해하지 않으면서 결과를 전달합니다.

> ⚠️ **같은 가이드 안에서 모순됩니다.** Overview 는 "화면 하단", 아래 Position 절은
> "화면 **상단** 중앙에 고정" 이라고 합니다. Position 절이 수치까지 갖춘 최신 내용으로 보입니다.
> → [확인 필요](#확인-필요)

##### 세부 — **TBD(투명도 50%)** `[?]`

> - 자동으로 사라지는 비침투적(Non-intrusive) 알림
> - 별도의 닫기 동작 없이도 소멸 (`showClose` 로 수동 닫기 가능)
> - 화면 상단 중앙에 배치 권장
> - 표시 시간: 일반 **3초**, 긴 메시지 **5초** 권장

#### 2. Spec

> 토스트(Toast)의 구조와 속성을 정의합니다.

**Anatomy** — 4개 요소

| 요소 | 설명 |
|---|---|
| `Icon` | 상태를 시각적으로 전달하는 아이콘 (**16×16**) |
| `Message` | 사용자에게 전달할 피드백 메시지 |
| `Close` | 수동 닫기 버튼 (**선택**, 16×16) |
| `Container` | `inverse-strong` 배경, `overlay` 그림자, `rounded/md` |

**Variants · Show Icon · Show Close** — `showIcon` / `showClose` 로 아이콘·닫기 버튼 노출을 제어합니다.

**Position**

> Toast는 화면 **상단 중앙에 고정**(`position: fixed`)되어 표시됩니다. Desktop에서는 GNB 하단 12px,
> Mobile에서는 Top Nav 하단 8px 아래에 위치하며, **띠배너 유무에 따라 top 값이 조정**됩니다.

| 항목 | Desktop | Mobile |
|---|---|---|
| 수평 정렬 | 화면 중앙 (center) | 화면 중앙 (center) |
| 수직 기준 | 띠배너 + GNB 하단에서 **12px** 아래 | 띠배너 + Top Nav 하단에서 **8px** 아래 |
| CSS 포지션 | `position: fixed` | `position: fixed` |
| `top` (띠배너 있을 때) | **133px** (띠배너 40 + GNB 81 + 여백 12) | **96px** (띠배너 36 + TopNav 52 + 여백 8) |
| `top` (띠배너 없을 때) | **93px** (GNB 81 + 여백 12) | **60px** (TopNav 52 + 여백 8) |
| `z-index` | 최상위 (**모달보다 위**) | 최상위 |

**Interaction**

> Toast는 아래에서 위로 **20px 슬라이드**하며 페이드 인으로 등장하고, **3~5초**간 유지된 후
> 위로 20px 이동하며 페이드 아웃으로 퇴장합니다.
> 등장과 퇴장 모두 **0.6초**간 `cubic-bezier(0.16, 1, 0.3, 1)` 이징이 적용됩니다.

이 파일에서 **이징 곡선과 지속 시간이 명시된 유일한 컴포넌트**입니다.

#### 3. Usage

> 토스트(Toast)의 올바른 사용 방법을 안내합니다.

`Do` / `Don't` 두 절로 예시를 보여줍니다. `[?]` 각 예시의 문구는 미조사입니다.

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

## `BottomSheet(Usage)` `1170:5163` — Bottom Sheet 두 번째 가이드 `[F]`

> **2026-10-15 개명 완료** — 프레임 이름이 `Search(Usage)` 였으나 내용과 맞지 않아
> **`BottomSheet(Usage)` 로 변경**했습니다.

`1600 × 9388` 프레임이며, 안의 제목은 다음과 같습니다.

> # Bottom Sheet Usage Guide
> 바텀시트(Bottom Sheet)의 사용 예시를 안내합니다.

프리뷰도 전부 `bottom_sheet` 인스턴스(`dimmer` + `open` → `bottom_sheet__atomic` ·
`content_area` · `button_area`)이며, 검색 필드는 한 번도 나오지 않습니다.

> `[?]` 이 프레임은 아직 **페이지 최상위**에 있습니다. 다른 가이드는 모두 해당 컴포넌트 프레임
> 안에 들어가 있으므로, [Bottom Sheet](#bottom-sheet-106518681) 프레임 안으로 옮기는 편이 일관됩니다.
> 재배치는 레이아웃에 영향을 줄 수 있어 적용하지 않았습니다.

### 절 구성

#### 1. State `1170:5169`

바텀시트의 세로 구조를 세 영역으로 나눕니다.

| 영역 | 동작 |
|---|---|
| Header (핸들바 + `direction/chevron` 뒤로 + 타이틀 + `suggested/close` 닫기) | **Sticky** |
| 콘텐츠 영역 | **Scrollable Area** |
| 하단 버튼 영역 | **Sticky** |

타이틀 샘플 문구: **"타이틀 최대 두 줄 스물여섯자 입력"**

#### 2. Spec `1170:5195`

| 항목 | 값 |
|---|---|
| **Container** `1170:5198` | **Max Height 90%** · **Flexible Width** |
| **Header Text** `1170:5210` | 해상도 **430 / 360 / 320** 세 폭에서 검증 |

최소 폭 320에서도 타이틀 26자가 두 줄 안에 들어가도록 잡혀 있습니다.

> Dialog 는 "최대 높이는 화면 높이 기준 **20% 여백**"(= 최대 80%), Bottom Sheet 는 **최대 90%** 로
> 서로 다릅니다.

#### 3. Behavior `1171:6187`

**Appear/Disappear** `1171:6190`
> \[닫기\]버튼 또는 dimmer를 탭할 시 모달이 사라집니다.

**Expandable** `1171:6321`
> - 상단의 핸들바를 드래그하면 화면을 확장할 수 있습니다.
> - 콘텐츠 길이에 따라 전체 화면까지 확장됩니다.
> - 스크롤이 최상단일 때 핸들바를 아래로 드래그하면 시트를 닫을 수 있습니다.

**Not Expandable** `1171:6653` — 프리뷰 두 개: `Dismissable` / `Not dismissable`
> - 화면 확장이 불가능한 경우, 핸들바 드래그에 따른 닫힘 여부는 콘텐츠에 따라 다르게 적용됩니다.
> - 스크롤이 최상단일 때만 핸들바 드래그로 하단 시트를 닫을 수 있습니다.
> - 닫힘이 유효하지 않은 콘텐츠에서는 바텀시트를 고정할 수 있습니다.

즉 **확장 가능 여부**와 **닫기 가능 여부**가 별개 축이며, 닫으면 안 되는 콘텐츠에서는 시트를 고정합니다.

#### 4. With Keyboard `1171:6777`

**Not Scrollable** `1171:6780`
> 키보드 노출 시, 모달은 키보드 높이만큼 상단으로 이동합니다.

**Scrollable** `1171:8518`
> 키보드가 표시된 이후 하단 시트가 일부 가려질 경우, 사용자가 모달 내 콘텐츠를 모두 확인할 수 있도록
> 콘텐츠 영역에 스크롤이 가능해야 합니다.

프리뷰는 `Keyboards / iPhone`(높이 218) 인스턴스를 얹어 보여줍니다.

> `[?]` 네 절의 `Description` 텍스트 노드는 모두 **hidden** 처리돼 있습니다. 위 문장들은
> 각 Text Sample 의 Label/Title 에 적힌 것입니다.

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
| 8 | `Sheet(Usage)` 부제는 Action Area 를 언급하는데 내용에는 Height 절만 있음 |
| 9 | **Toast Overview 의 "화면 하단" ↔ Position 의 "화면 상단 중앙" 모순** |
| 10 | Usage 가이드가 **없는** 오버레이: Tooltip · Snack Bar · Popup · System message · Pulldown menu |
| 11 | ~~`Search(Usage)` 프레임명 불일치~~ → **2026-10-15 `BottomSheet(Usage)` 로 개명 완료** |
| 13 | Toast `Usage` 절의 Do / Don't 예시 문구 미조사 |
| 14 | `Sheet(Usage)` 개명·축소 후 내용 재확인 |
| 15 | Bottom Sheet 가이드가 **두 개**(`Sheet(Usage)` + `BottomSheet(Usage)`) — 통합 여부 결정 필요 |
| 16 | `BottomSheet(Usage)` 가 페이지 최상위에 있음 — Bottom Sheet 프레임 안으로 이동 권장 |
| 12 | 바텀시트 최대 높이가 파일 안에서 **90%**(`Search(Usage)` Spec)와 **80%**(`Sheet(Usage)` Height)로 갈림 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
