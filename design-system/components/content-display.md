# Content Display `[F]`

> 출처 — Figma 페이지 **• Content Display** `1595:11126`, Overview 표 `1192:7647`
> 베리언트 이름은 Figma 컴포넌트 세트의 프로퍼티 조합 그대로입니다.

## Overview 상태표

| 컴포넌트 | Status | Last Update |
|---|---|---|
| Accordion | In-progress | N/A |
| Avatar | Before | N/A |
| Draggable list | Before | N/A |
| List | In-progress | 1/26/26 |
| Thumbnail | Done | N/A |
| Image grid | Before | N/A |
| Cards | Done | 2/2/26 |
| Video player | Before | N/A |
| Data table | Before | N/A |

> 상세 페이지의 실제 구성은 이 표와 다릅니다 → [README.md](README.md#overview-표와-상세-페이지의-목록이-다릅니다-)

---

## 컴포넌트 프레임 하단의 `(Usage)` 가이드 `[F]`

일부 컴포넌트는 프레임 **하단에 `<이름>(Usage)` 가이드**를 갖습니다. 구조는 모두 같습니다.

```
Guide                       ← "<컴포넌트 한글명>(<영문명>)의 사용 예시를 안내합니다."
└ <컴포넌트명>
   ├ <프로퍼티 섹션>  [Desktop / Mobile 칩]
   │   설명 문장
   │   └ Preview — 값별 예시 + 값 라벨 칩
   └ …
```

### 여기서만 드러나는 사실 — 베리언트가 아닌 프로퍼티

컴포넌트 세트의 **베리언트 이름**(`size=lg, textAlign=left` 등)에는 나타나지 않지만,
Usage 가이드에는 등장하는 프로퍼티가 있습니다. Figma의 **boolean / instance-swap 프로퍼티**로
보이며, 베리언트 목록만 읽으면 놓치게 됩니다.

| 컴포넌트 | 베리언트 프로퍼티 | Usage 가이드에만 있는 프로퍼티 |
|---|---|---|
| Thumbnail `Ratio` | `ratio`, `color` | **`showDimmer`** |
| Label | `size`, `textAlign` | **`showCount`**, **`required`** |
| EventCard | `viewport`, `status` | **`showSubtitle`** |
| CartItem | `viewport`, `state` | **`checked`** (가이드 표기 `Checked`), `type` |

구현 시 props를 베리언트 목록만 보고 정의하면 이 항목들이 누락됩니다.

---

## 상세 페이지의 컴포넌트 11종

### Accordion `1621:13143`

| 프로퍼티 | 값 |
|---|---|
| `type` | `info` · `contents` |
| `size` | `lg` · `md` · `sm` |
| `expand` | `true` · `false` |

베리언트 12개 (2 × 3 × 2).

### Avatar `1621:13663`

| 프로퍼티 | 값 |
|---|---|
| `size` | `xs` · `sm` · `md` · `lg` · `xl` |
| `type` | `empty` · `text` · `image` |
| `state` | `default` · `overlay` |

베리언트 30개 (5 × 3 × 2).

### Carousel `1621:19606`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Carousel` | `type=horizontal \| vertical` |
| `└ Swiper` (atomic) | `arrow=left \| right \| up \| down`, `state=default \| hover \| disabled` |

### OptionRow `3445:9254`

| 프로퍼티 | 값 |
|---|---|
| `viewport` | `desktop` · `mobile` |
| `showOption` | `true` · `false` |
| `isDisabled` | `true` · `false` |

### Price `3432:15991`

| 프로퍼티 | 값 |
|---|---|
| `type` | `info` · `product` · `cart` |
| `size` | `lg` · `md` |
| `currency` | `KRW` · `USD` · `JPY` |
| `discout` ※오타 | `true` · `false` |

베리언트 36개 (3 × 2 × 3 × 2). 프로퍼티 이름 `discout` 는 **Figma 원문 그대로의 오타**입니다(`discount`).

**다중 통화(KRW / USD / JPY)를 토큰 레벨이 아니라 컴포넌트 베리언트로 다룹니다.**

### Label `1621:17834`

| 프로퍼티 | 값 |
|---|---|
| `size` | `xs` · `sm` · `md` · `lg` |
| `textAlign` | `left` · `center` · `right` |

프레임 안에 `Default Label` / `Hover Label` / `Disabled Label` 상태 예시와 `Tertiary Sizes` 블록,
그리고 `Label(Usage)` 프레임이 있습니다.

> Change Log `260204`: **"required" 필수 입력/선택 표시 추가.**

#### 사용 가이드 — `Label(Usage)` `1621:17816`

> **Guide** — 레이블(Label)의 사용 예시를 안내합니다.

| 섹션 | 뷰포트 칩 | 시안 설명 (원문) |
|---|---|---|
| **Text Align** | Desktop | 레이블 텍스트의 정렬 방향을 설정합니다. left, center, right 옵션을 지원합니다. |
| **Show Count** | — | *(설명 문장 없음)* |

`Show Count` 프리뷰는 `레이블 0 *` 형태로, **레이블 텍스트 + 카운트 숫자 + 필수 표시(`*`)** 를
함께 보여줍니다. 필수 표시는 빨간색이며 Change Log `260204`의 `required` 항목과 이어집니다.
사이즈 4단계(`lg`/`md`/`sm`/`xs`)를 행으로 나열합니다.

### List `1621:15994`

여러 하위 컴포넌트를 묶은 프레임입니다.

| 하위 컴포넌트 | 프로퍼티 |
|---|---|
| `TextList` | `type=default` |
| `└ TextList-atomic` | `type=up \| down \| none \| new`, `active=true \| false` |
| `LogoList` | `direction=vertical \| horizontal` |
| `└ LogoList-atomic` | `type=기본` |
| `List/menu` | `Type=Features` |
| `List Item/menu` | `type=feature item \| category menu item` |
| `List/category` | `Type=대분류 \| 중분류`, `Screen=mobile \| desktop` (`대분류` 는 mobile만) |
| `List Item/category` | `type=대분류, selected=True\|False` · `type=중분류, selected=default` |

> 베리언트 값에 한글(`기본`, `대분류`, `중분류`)이 쓰이고, boolean 표기가 `True/False`(대문자)와
> `true/false`(소문자)로 섞여 있습니다. → [naming.md](../guidelines/naming.md)

### Thumbnail `1621:13882`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Ratio` | `ratio=1:1 \| 1.618:1 \| 16:9`, `color=brand \| gray` |
| `ImageGallery` | `color=brand \| gray`, `state=default \| hover \| selected` |

`Thumbnail(Usage)` 프레임(`2980:8714`)에서 `ratio` · `color` · `showDimmer=true|false` 조합을 예시로 보여줍니다.

> `[?]` 이 프레임 안에 `sfhsfh`, `eryetyeyh`, `Stateㅁ파ㅜ미ㅏㅣㅏㅁ이ㅏㅠs Header` 같은
> **키보드 입력 실수로 보이는 레이어 이름**이 남아 있습니다. 정리 필요.

#### 사용 가이드 — `Thumbnail(Usage)` `2980:8714`

> **Guide** — 썸네일(Thumbnail)의 사용 예시를 안내합니다.

`Ratio` 컴포넌트에 대해 세 가지 프로퍼티를 설명합니다.

| 섹션 | 시안 설명 (원문) | 값 |
|---|---|---|
| **Color** | color 속성으로 brand와 gray 두 가지 컬러 테마를 선택할 수 있습니다. | `brand` · `gray` |
| **Ratio** | ratio 속성으로 이미지 비율을 1:1, 1.618:1, 16:9 중 선택할 수 있습니다. | `1:1` · `1.618:1` · `16:9` |
| **Show Dimmer** | showDimmer 속성을 활성화하면 이미지 위에 **SOLD OUT 딤 처리**가 적용됩니다. | `true` · `false` |

`showDimmer=true` 는 단순 어둡게 처리가 아니라 **품절(SOLD OUT) 표현**입니다.
장바구니의 구매 불가 상품(`CartItem` `Disabled`)에서도 같은 표현을 씁니다.

> `[?]` Color 섹션의 값 칩이 `color true` / `color gray` 로 찍혀 있습니다.
> 베리언트 값은 `brand` / `gray` 이므로 `true` 는 `brand` 의 오기로 보입니다.

### Table `1621:13945`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Table` | `viewport=desktop, type=horizontal, columns=1\|2` · `viewport=desktop, type=vertical, columns=3\|4` · `viewport=mobile, type=horizontal, columns=1\|2` |
| `└ Table-row` | `viewport=desktop, columns=1~4` · `viewport=mobile, columns=1~2` |
| `└ Table-atomic` | `type=head \| body`, `size=lg \| md \| sm` |

`type=horizontal` 은 columns 1–2, `type=vertical` 은 columns 3–4 조합만 존재합니다.
모바일은 columns 1–2 (horizontal)만 있습니다.

### Text List `1621:13964`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `└ List-atomic` | `level=1 \| 2` |
| `└ Bullet` | `type=circle \| hypen` ※오타(`hyphen`) |
| `TextList` | `level=level2` |

### Card `1621:19898` — 가장 큰 컴포넌트 군

`7872 × 14428` 크기의 프레임으로, 5종 카드 + 원자 컴포넌트들로 구성됩니다.

#### ProductCard
| 컴포넌트 | 프로퍼티 |
|---|---|
| `ProductCard` | `viewport=desktop \| mobile` |
| `└ ProductWish-atomic` | `size=lg \| sm`, `selected=true \| false` |
| `└ ProductTitle-atomic` | `size=lg \| md`, `textLines=1 \| 2` |

#### InfoCard
| 컴포넌트 | 프로퍼티 |
|---|---|
| `InfoCard` | `viewport=desktop \| mobile`, `isDiscount=true \| false`, `isOverseas=true \| false` |
| `└ InfoBenefit-atomic` | `viewport`, `type=default \| benefit`, `expanded=true \| false` (`default` 는 `expanded=false` 만) |
| `└ InfoOption-atomic` | `size=md \| sm`, `state=default \| hover \| disabled`, `selected=True \| False` |
| `└ InfoCoupon-atomic` | *(베리언트 없음)* |

`isOverseas` — 해외 배송 상품 표시. 관련 UI로 `Import Duty`(관세) · `Shipping Fee` · `Weight Info` 블록이 있습니다.

#### ProfileCard
| 컴포넌트 | 프로퍼티 |
|---|---|
| `ProfileCard` | `size=lg \| md`, `state=default \| hover \| pressed \| disabled` |
| `└ ProfileWish-atomic` | `size=lg \| sm`, `pressed=true \| false` |

#### EventCard
| 프로퍼티 | 값 |
|---|---|
| `viewport` | `desktop` · `mobile` |
| `status` | `upcoming` · `ongoing` · `ended` |

#### CartItem
| 프로퍼티 | 값 |
|---|---|
| `viewport` | `desktop` · `mobile` |
| `state` | `default` · `selected` · `disabled` |

#### 사용 가이드 — `Card(Usage)` `2582:8855`

`7712 × 9511` 크기로, 카드 종류별 절을 갖습니다. 각 절의 머리말이 그 카드의 정의입니다.

| 절 | 노드 | 시안 설명 (원문) |
|---|---|---|
| **Product Card** | `2582:8859` | 조합에 따라 다양한 형태의 속성이 존재합니다. |
| **Information Card** | `2613:3493` | 이미지·가격·옵션 정보를 함께 제공하는 카드로, 다양한 프로퍼티가 존재합니다. |
| **Profile Card** | `2618:4647` | 아바타와 타이틀·서브타이틀로 구성된 카드로, 크기와 상태 프로퍼티가 존재합니다. |
| **Event Card** | `3476:9796` | Event Card는 **Sphere(스피어)의 정보를 나타내는 카드**로, **스피어 탭의 이벤트 내용**을 나타내는 요소로 사용합니다. |
| **Cart Item** | `3476:10039` | 장바구니 화면에서 선택한 상품의 정보를 표시하는 카드입니다. 상품 이미지, 상품명, 가격, 수량 조절, 옵션 표시 등의 기능을 포함합니다. |

##### Event Card `3476:9796`

| 섹션 | 시안 설명 (원문) | 값 |
|---|---|---|
| **Viewport** | Desktop과 Mobile 뷰포트에 따라 **카드 크기**를 조정합니다. | `Desktop` · `Mobile` |
| **Status** | 이벤트의 상태(예정/진행 중/종료)에 따라 카드의 시각적 표현이 변경됩니다. | `Upcoming` · `Ongoing` · `Ended` |
| **Show Subtitle** | 서브타이틀의 표시 여부를 설정합니다. | `True` · `False` |

상태별 표현(프리뷰 실측):

| status | 배지 | 이미지 | 텍스트 |
|---|---|---|---|
| `upcoming` | **예정** — 연한 배경 배지 | 기본 | 기본 |
| `ongoing` | **진행중** — 어두운(검정) 배지 | 밝은 회색 | **날짜가 브랜드 컬러** |
| `ended` | **종료** — 연한 배지 | **어둡게 딤** | 전체 흐림(disabled 계열) |

날짜는 `202Y.MM.DD — MM.DD` 형식이며 `editor/calendar` 아이콘이 앞에 붙습니다.

> **Sphere(스피어)** 라는 도메인 개념이 이 가이드에서 처음 등장합니다. `[?]` 정의는 시안에 없습니다.

##### Cart Item `3476:10039`

| 섹션 | 시안 설명 (원문) | 값 |
|---|---|---|
| **Viewport** | Desktop과 Mobile 뷰포트에 따라 **카드의 레이아웃**이 변경됩니다. | `Desktop` · `Mobile` |
| **Type** | 상품의 구매 가능 상태에 따라 Default와 Disabled 타입으로 구분됩니다. | `Default` · `Disabled` |
| **Checked** | 체크박스를 통해 상품의 선택 상태를 나타냅니다. | `True` · `False` |

`Disabled` 는 썸네일에 **SOLD OUT 딤**(= `Thumbnail` 의 `showDimmer`)이 적용되고,
상품명·가격·옵션·수량 스테퍼가 모두 흐려지며 체크박스가 비활성화됩니다.

> `[?]` 가이드의 `Type`(Default/Disabled)·`Checked` 와 컴포넌트 세트의 베리언트
> `state=default | selected | disabled` 가 서로 다른 축입니다. `selected` 가 `checked=true` 에
> 대응하는지 확인이 필요합니다.

→ 화면 조합은 [../patterns/commerce.md](../patterns/commerce.md)

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | Overview 표와 상세 페이지의 컴포넌트 목록 불일치 (`Draggable list`, `Image grid`, `Video player` 는 상세 없음 / `Carousel`, `Price`, `OptionRow`, `Label`, `Text List` 는 Overview 표에 없음) |
| 2 | `Price` 의 프로퍼티 오타 `discout` |
| 3 | `Bullet` 의 값 오타 `hypen` |
| 4 | 베리언트 boolean 표기 혼용 — `true/false` vs `True/False` |
| 5 | 베리언트 값에 한글 사용 (`type=기본`, `Type=대분류`) — 코드 매핑 규칙 필요 |
| 6 | Thumbnail 프레임의 무의미한 레이어 이름 잔재 |
| 7 | 각 컴포넌트의 `Version Info` · `Develop Info` 본문은 미조사 |
| 8 | `CartItem` 의 `Type`/`Checked`(가이드) ↔ `state`(베리언트) 축 불일치 |
| 9 | Usage 가이드가 **없는** 컴포넌트: Accordion · Avatar · Carousel · OptionRow · Price · List · Table · Text List |
| 10 | `Sphere(스피어)` 도메인 용어의 정의 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
