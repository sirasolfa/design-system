# 디자인팀 요청 사항

> 작성일 **2026-10-15** · 대상 Figma [NDS - NOVERA Design System](https://www.figma.com/design/OJqTwQ8gHDGcvOOkOfYRgM/NDS---NOVERA-Design-System?node-id=0-1) (`OJqTwQ8gHDGcvOOkOfYRgM`)
> 이 문서는 **개발이 코드로 옮기기 위해 디자인 확인·보완이 필요한 항목**을 모은 것입니다.
> 모든 항목에 노드 ID를 붙였습니다. Figma에서 `⌘/` → 노드 ID 붙여넣기로 바로 이동할 수 있습니다.

> **2026-10-15 진행** — B-1(레이어명 `Search(Usage)` → `BottomSheet(Usage)`)은 **개발 측에서 직접 적용 완료**했습니다.
> 같은 날 확인에서 **Toast 가이드가 새로 작성된 것**(`4493:25180`)도 발견해 아래 E-1 을 정정했습니다.

| 분류 | 건수 | 성격 |
|---|---|---|
| [A. 사용 가이드 없음](#a-사용-가이드가-없는-컴포넌트) | 11 + 24 | 신규 작성 요청 |
| [B. 이름 ↔ 내용 불일치](#b-이름--내용-불일치) | 2 | 레이어명 정정 |
| [C. 값이 서로 다름](#c-같은-값이-파일-안에서-다르게-적힘) | 6 | 정본 확정 |
| [D. 오타](#d-오타) | 11 | 일괄 정정 |
| [E. 미완 상태](#e-비어-있거나-tbd-인-것) | 2 | 상태 공유 |

---

## A. 사용 가이드가 없는 컴포넌트

프레임 하단의 `<이름>(Usage)` 가이드가 있는 컴포넌트는 **10종**입니다.
나머지는 베리언트 목록만 있어, 개발이 **각 프로퍼티를 언제 쓰는지 알 수 없습니다.**

### A-1. 가장 급한 것 — 상태가 `Done` 인데 가이드가 없음 (11종)

이미 완료로 표시돼 있어 개발이 바로 착수할 수 있는데, 사용 규칙이 없습니다.

| 컴포넌트 | 카테고리 | Last Update | 상세 프레임 |
|---|---|---|---|
| Bottom navigation | Navigation | 1/21/26 | 없음 |
| Link (링크버튼!) | Navigation | N/A | 없음 |
| Top navigation_mobile | Navigation | 1/23/25 | 없음 |
| Top navigation_desktop | Navigation | 1/26/26 | 없음 |
| Page Indicator | Navigation | 2/05/26 | 없음 |
| Badge | Indicator & Status | 1/22/25 | 없음 |
| Push badge | Indicator & Status | 1/26/26 | 없음 |
| Text area | Inputs | N/A | 없음 |
| Text input | Inputs | N/A | 없음 |
| Search | Inputs | N/A | 없음 |
| Snackbar | Overlays | 1/27/26 | `1384:7161` |

> Toast(Done, 1/27/26)는 10-15 확인 시점에 가이드가 작성돼 있어 위 목록에서 제외했습니다.

> **Text input / Text area** 는 Change Log 에 높이(56/44/32)와 `state: filled`, `showTrailingIn`
> 변경만 적혀 있고, state 전체 목록(default/focus/error/disabled)과 에러 메시지 규칙이 없습니다.
>
> **Badge** 는 다른 컴포넌트(Card, Drawer) 안에서 이미 인스턴스로 쓰이는데 타입·사이즈 정의가 없습니다.

### A-2. 상세 프레임은 있으나 가이드가 없음 (7종)

| 컴포넌트 | 노드 | 베리언트 수 | 비고 |
|---|---|---|---|
| **Tooltip** | `1600:13434` | **72** | 파일에서 베리언트가 가장 많은 컴포넌트. `direction`×`align`×`size`×`theme` 조합 기준이 없습니다 |
| Avatar | `1621:13663` | 30 | `size` 5 × `type` 3 × `state` 2 |
| Carousel | `1621:19606` | 2 + 12 | `Swiper` 화살표 `state` 포함 |
| List | `1621:15994` | 복합 | `TextList`·`LogoList`·`List/menu`·`List/category` 4계열이 한 프레임에 |
| Table | `1621:13945` | 복합 | `type=horizontal` 은 columns 1–2, `vertical` 은 3–4 인 이유가 불명확 |
| Text List | `1621:13964` | 4 | `level` · `Bullet type` |
| Snack Bar | `1384:7161` | 3 | A-1 과 중복 |

### A-3. 상세 프레임 자체가 없음 (카테고리 4개, 총 32종)

Figma 파일에 페이지가 **4개**(Overview · Foundation · • Content Display · • Overlay)뿐이라,
아래 카테고리는 Overview 상태표에만 존재합니다.

| 카테고리 | 종수 | Overview 노드 |
|---|---|---|
| Navigation | 9 | `1183:7464` |
| Button | 2 | `1192:6212` |
| Inputs | 13 | `1192:7929` |
| Indicator & Status | 8 | `1192:7796` |

> Overview 표에서 컴포넌트 이름에 **밑줄(링크)** 이 있는 항목들이 있습니다.
> 다른 파일로 연결되는 것이라면 **그 파일 링크를 알려주세요.** 개발이 참조할 곳이 없습니다.

### 요청

1. **A-1 11종**부터 가이드를 만들어 주세요. 완료 표시된 것부터 개발이 착수합니다.
2. 가이드 형식은 기존 것과 동일하게 — `Guide` 제목 + `<한글명>(<영문명>)의 사용 예시를 안내합니다.`
   + 프로퍼티별 절(절 제목 + 설명 한 줄 + 프리뷰).
   **[`Accordion(Usage)`](https://www.figma.com/design/OJqTwQ8gHDGcvOOkOfYRgM/NDS---NOVERA-Design-System?node-id=4073-12234) `4073:12234` 가 가장 좋은 예시**입니다(속성 10개를 한 절씩).
3. 특히 **베리언트에 안 드러나는 프로퍼티**(boolean / 텍스트 / Instance Swap / Slot)는
   가이드에만 나오므로 빠짐없이 적어 주세요. → [B 참고](#개발이-가이드에-의존하는-이유)

### 개발이 가이드에 의존하는 이유

컴포넌트 세트의 **베리언트 이름만으로는 프로퍼티의 절반도 알 수 없습니다.**

| 컴포넌트 | 베리언트 | 가이드에만 있는 프로퍼티 |
|---|---|---|
| **Accordion** | `type`, `size`, `expand` (3) | `showLeadingIcon`(+`└ leadingIcon` Instance Swap), `showBodyTxt`, `showBadge`, `showTopDivider`, `showBottomDivider`, `showSubItems`, Slot `addSubRow`, Slot `addSubAccordion` (**8**) |
| Price | `type`, `size`, `currency`, `discout` | `price`, `discountPrice`, `originalPrice` |
| OptionRow | `viewport`, `showOption`, `isDisabled` | `isDiscount`, `optionName` |
| Thumbnail | `ratio`, `color` | `showDimmer` |
| Label | `size`, `textAlign` | `showCount`, `showRequired`, `color`, `text` |
| EventCard | `viewport`, `status` | `showSubtitle` |
| CartItem | `viewport`, `state` | `checked`, `type` |

가이드가 없으면 이 프로퍼티들이 **코드에서 통째로 누락**됩니다.

---

## B. 이름 ↔ 내용 불일치

가이드 **12개 전부**의 프레임 이름과 내부 제목을 대조했습니다. 2건이 어긋납니다.

| 프레임명 | 노드 | 내부 제목 / 부제 | 판정 |
|---|---|---|---|
| ~~`Search(Usage)`~~ → **`BottomSheet(Usage)`** | `1170:5163` | **Bottom Sheet Usage Guide** / 바텀시트(Bottom Sheet)의 사용 예시를 안내합니다. | ✅ **개명 완료 (10-15)** |
| **`Sheet(Usage)`** | `3572:31464` | Guide / **액션 영역(Action Area)과** 바텀시트 높이 규칙의 사용 예시를 안내합니다. | ⚠️ **부제 정정 필요** |
| `Toast(Usage)` | `4493:25180` | Guide / 토스트(Toast)의 사용 예시를 안내합니다. | ✅ |
| `Dialog(Usage)` | `4805:36820` | Guide / 다이얼로그(Dialog)의 사용 예시를 안내합니다. | ✅ |
| `Drawer(Usage)` | `1358:8391` | Drawer Usage Guide / 드로어(Drawer)의 사용 예시를 안내합니다. | ✅ |
| `Accordion(Usage)` | `4073:12234` | Guide / Accordion 컴포넌트의 속성별 사용법을 안내합니다. | ✅ |
| `Price(Usage)` | `4703:13314` | Guide / 가격(Price)의 사용 예시를 안내합니다. | ✅ |
| `OptionRow(Usage)` | `4726:13681` | Guide / 옵션 행(OptionRow)의 사용 예시를 안내합니다. | ✅ |
| `Thumbnail(Usage)` | `2980:8714` | Guide / 썸네일(Thumbnail)의 사용 예시를 안내합니다. | ✅ |
| `Label(Usage)` | `1621:17816` | Guide / 레이블(Label)의 사용 예시를 안내합니다. | ✅ |
| `Card(Usage)` | `2582:8855` | Guide / 카드(Card)의 사용 예시를 안내합니다. | ✅ |
| `Event Card(Usage)` | `3476:9796` | Event Card / Event Card는 Sphere(스피어)의 정보를 나타내는 카드로… | ✅ |
| `Cart Item(Usage)` | `3476:10039` | Cart Item / 장바구니 화면에서 선택한 상품의 정보를 표시하는 카드입니다. | ✅ |

### B-1. `Search(Usage)` → `BottomSheet(Usage)` ✅ 완료

`1170:5163` (`1600 × 9388`) 은 **이름만 Search** 이고, 내용은 전부 바텀시트입니다.

- 내부 제목: **"Bottom Sheet Usage Guide"**
- 4개 절: `State` · `Spec` · `Behavior` · `With Keyboard`
- 프리뷰 전원 `bottom_sheet` 인스턴스 (`dimmer` + `open` → `bottom_sheet__atomic` · `content_area` · `button_area`)
- **검색 필드는 한 번도 등장하지 않습니다**

이 때문에 개발 문서에 한 차례 "Search 가이드"로 잘못 적혔다가 정정했습니다.
**2026-10-15 에 `BottomSheet(Usage)` 로 개명했습니다.**

**남은 요청** — 이 프레임은 여전히 Bottom Sheet 컴포넌트 **안이 아니라 페이지 최상위**에 떠 있습니다.
다른 가이드 12개는 모두 해당 컴포넌트 프레임 안에 들어가 있습니다.
**Bottom Sheet 프레임(`1065:18681`) 안으로 옮겨 주세요.**
(재배치는 레이아웃에 영향을 줄 수 있어 개발 측에서 임의로 적용하지 않았습니다.)

### B-2. `Sheet(Usage)` 부제와 내용이 맞지 않음

부제는 "**액션 영역(Action Area)과** 바텀시트 높이 규칙"이라고 하는데,
현재 `Content`(`3572:31468`) 안에는 **`Height` 절 하나뿐**입니다.

이전에 있던 **Button Pair · Button Action Bar · Action Area 세 절이 사라졌습니다.**
(프레임도 `Action Area(Usage)` → `Sheet(Usage)` 로 개명되며 1870 → 1637 로 축소)

- 다른 곳으로 옮기신 거라면 **어디로 갔는지** 알려주세요.
- 삭제하신 거라면 **부제에서 "액션 영역(Action Area)과" 를 빼 주세요.**
- `ButtonPair` / `ButtonActionBar` 는 Dialog·Bottom Sheet 양쪽에서 쓰이므로,
  **독립 가이드로 분리**하는 편이 맞아 보입니다.

### B-3. 가이드 제목 형식이 세 가지로 갈립니다

| 형식 | 쓰는 곳 |
|---|---|
| `Guide` | Dialog · Accordion · Price · OptionRow · Thumbnail · Label · Card · Sheet |
| `<이름> Usage Guide` | Drawer · Bottom Sheet(= `Search(Usage)`) |
| 컴포넌트명 그대로 | Event Card · Cart Item |

부제 문구도 `…의 사용 예시를 안내합니다` / `…컴포넌트의 속성별 사용법을 안내합니다` 두 가지입니다.
**하나로 통일해 주시면** 개발이 가이드를 기계적으로 찾아낼 수 있습니다
(현재는 프레임 이름을 믿을 수 없어 매번 내부 제목을 열어 확인하고 있습니다).

---

## C. 같은 값이 파일 안에서 다르게 적힘

개발이 어느 쪽을 따라야 할지 정해 주셔야 합니다.

### C-1. 바텀시트 최대 높이 — 90% vs 80% ❗

| 출처 | 값 |
|---|---|
| `Search(Usage)` > Spec > Container (`1170:5198`) | **Max Height 90%** |
| `Sheet(Usage)` > Height (`4806:7119`) | **화면 높이의 80%**, 최소 200px |

`Sheet(Usage)` 쪽이 "모달과 동일하게 상단 20%를 남기며"라고 Dialog 와 맞춰 설명하고 있어
80% 가 최신으로 보이지만, 90% 표기도 그대로 남아 있습니다.

### C-2. `layout.spacing` 스케일 — 라벨이 한 칸 밀린 것으로 보임

Layout 페이지(`170:1666`)에 **인쇄된 라벨**과 **변수 실제값**이 다릅니다.

| 토큰 | 인쇄된 라벨 | 변수 실제값 |
|---|---|---|
| `xl` | 32px | **28** |
| `2xl` | 40px | **32** |
| `3xl` | 48px | **40** |

그리고 문서에 없는 단계가 더 있습니다 — `6xs`(2) · `5xs`(4) · `4xs`(6) · `4xl`(48) · `5xl`(64).
**인쇄 라벨 32/40/48 이 `2xl`/`3xl`/`4xl` 의 실제 값과 정확히 일치**하므로,
표가 한 칸 밀려 적힌 것으로 보입니다. 확인 후 스와치 전체를 갱신해 주세요.

### C-3. `color.border.strong` / `.disabled` 매핑이 뒤바뀜

| 토큰 | Semantic 표 매핑 | 변수 실제값 |
|---|---|---|
| `color.border.strong` | `gray/300` | `#c5c9d3` = **gray/400** |
| `color.border.disabled` | `gray/400` | `#e3e6ee` = **gray/300** |

표대로면 "더 진한 테두리"라는 `strong` 의 설명과 어긋납니다. 변수 쪽이 맞아 보입니다.

### C-4. gray 리넘버링이 Semantic 표에 미반영

Change Log `251224` 의 `gray 50→100, 100→150` 이후, 아래 라벨이 옛 번호로 남아 있습니다.

| 토큰 | 표 라벨 | 실제 |
|---|---|---|
| `color.text.primary` | gray/900 | gray/**950** |
| `color.bg.subtle` | gray/50 | gray/**100** |
| `color.bg.muted` | gray/100 | gray/**150** |
| `color.divider.soft` | gray/100 | gray/**150** |

### C-6. Toast 배치 — "화면 하단" vs "화면 상단 중앙" ❗

같은 `Toast(Usage)` `4493:25180` 안에서 어긋납니다.

| 절 | 문구 |
|---|---|
| **Overview** | 토스트(Toast)는 화면 **하단**에 잠시 나타났다가 자동으로 사라지는 피드백 UI입니다. |
| **Position** | Toast는 화면 **상단 중앙**에 고정(`position: fixed`)되어 표시됩니다. |
| Overview 세부(투명도 50%) | 화면 **상단** 중앙에 배치 권장 |

Position 절은 Desktop/Mobile 별 `top` 값(133/96/93/60px)까지 수치로 적혀 있어 최신으로 보입니다.
**Overview 문장의 "하단" 을 "상단" 으로 고쳐 주세요.**

### C-5. Semantic 표에 아예 없는 토큰 6종

컴포넌트가 실제로 쓰는데 Semantic Color Token 페이지(`144:419`)에 없습니다.
표에 추가해 주세요.

`color/bg/overlay/mask`(40%) · `color/bg/surface/neutral-soft` · `color/bg/surface/inverse` ·
`color/text/subtle`(`#464c53` — gray 팔레트 어느 단계와도 불일치) ·
`color/text/status/negative` · `color/background/white`(`color/bg/surface/default` 와 중복)

---

## D. 오타

코드 토큰으로 그대로 옮겨지면 영구히 남습니다. 일괄 정정 부탁드립니다.

| 현재 | 올바른 표기 | 위치 |
|---|---|---|
| `color.text.priamry` | `primary` | Semantic Color Token 표 |
| `color.divider.defualt` | `default` | Semantic Color Token 표 |
| `sementic/background/*` | `semantic` | 변수 컬렉션 |
| `discout` | `discount` | **Price 프로퍼티 · `Price(Usage)` 절 제목 · 컴포넌트 설명 3곳 전부** |
| `hypen` | `hyphen` | Text List > Bullet `type` |
| `Postition` | `Position` | Toast 가이드 절 제목 |
| `Loading Cirlce` | `Circle` | Toast(Usage) 레이어 |
| `Lable` | `Label` | Snack Bar 레이어 |
| `Primitve Color Palette` | `Primitive` | Foundation 프레임명 |
| `System Conponent` | `Component` | Foundation 섹션명 |
| `showTrailingIn` | `showTrailingIcon` *(추정)* | Change Log Input Field `260202` |

> `Elevation` 설명의 "요소의 깊이감을 표현하는 **기복적인** 방법" 도 "기본적인" 오타로 보입니다.

---

## E. 비어 있거나 TBD 인 것

작업 중이라면 그대로 두셔도 됩니다. **개발이 "없는 것"과 "아직인 것"을 구분하려는 목적**입니다.

### E-1. Toast 가이드가 재작성됐습니다 — 내용 확인 요청 ✅→🔄

조사 도중 Toast 프레임(`1368:9769`)이 잠시 비어 있었는데, 같은 날 다시 확인하니
**`Toast(Usage)` `4493:25180`** (`1440 × 5193`) 가 새로 들어와 있었습니다.

| | 이전 (`1368:10031`) | 현재 (`4493:25180`) |
|---|---|---|
| 제목 | Guide / 토스트(Toast)의 사용 예시를 안내합니다. | 동일 |
| 첫 절 | `Element Patterns & Types` | **`Overview`** |

**절 구성이 바뀌어 개발 문서가 구버전 기준입니다.** 재작성이 끝난 상태인지 알려주시면
다시 읽어 문서를 갱신하겠습니다.

### E-2. `Sheet(Usage)` > Height 의 세부 규칙이 투명도 50%

`4805:37413` 불릿 5개가 `opacity: 0.5` 로 흐리게 처리돼 있습니다.
확정 전 초안으로 보고 **개발 문서에 TBD 로 표시**해 두었습니다. 확정되면 알려주세요.

내용: 높이 범위 정의 / 필수 영역·스크롤 처리 / 키보드 열렸을 때 재계산 /
짧은 화면에서 최대 높이 우선 / 812px 예시.

### E-3. 설명이 비어 있는 절

| 위치 | 상태 |
|---|---|
| `Toast(Usage)` > Behavior · Usage · Design Spec | 절 제목만 있고 설명 문장 없음 |
| `Search(Usage)` 4개 절 | `Description` 노드가 모두 **hidden** |
| `shape.rounded.xs`(6px) Role | `--` 로 비어 있음 (`260106` 에 새로 추가된 단계) |

---

## 참고 — 개발이 가이드를 읽는 방법

문서화 자동화를 위해 알아두시면 좋은 점입니다.

- 가이드 **설명 문장은 레이어 이름에 없습니다.** Figma MCP 의 `get_metadata` 로는
  `Guide` · `Section Title` · `Description` 같은 껍데기만 보여, 매번 스크린샷이나
  `get_design_context` 로 열어야 합니다.
- 반대로 **Accordion(Usage)** 는 설명 문장이 그대로 레이어 이름으로 들어가 있어
  (`type 속성으로 아코디언의 유형을 선택합니다…`) 자동 추출이 바로 됩니다. **이 방식이 가장 좋습니다.**
- **컴포넌트 설명(Description)** 을 Figma 컴포넌트에 달아두시면 개발이 자동으로 읽어갑니다.
  현재 `ButtonPair` · `└ OptionRow` · `└ Price` · `└ Label` · 아이콘 일부에 달려 있고 매우 유용합니다.
  나머지 컴포넌트에도 달아 주시면 가이드 프레임 없이도 최소한의 용도는 전달됩니다.
- **노드 ID 와 프레임 이름이 자주 바뀝니다.** 2026-09-02 → 10-15 사이에
  `Action Area(Usage)` → `Sheet(Usage)` 개명, 가이드 4종 신설, Toast 비워짐이 있었습니다.
  큰 구조 변경 시 알려주시면 문서를 맞춰 갱신하겠습니다.

---

관련 문서 — [컴포넌트 인벤토리](../components/README.md) · [Usage 가이드 목록](../patterns/README.md) · [네이밍 규칙](naming.md)
