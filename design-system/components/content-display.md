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

> 상세 페이지의 실제 구성은 이 표와 다릅니다 → [README.md](README.md#overview-표와-상세-페이지의-목록이-다릅니다)

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
| Label | `size`, `textAlign` | **`showCount`**, **`showRequired`**, `color`, `text` |
| EventCard | `viewport`, `status` | **`showSubtitle`** |
| CartItem | `viewport`, `state` | **`checked`** (가이드 표기 `Checked`), `type` |
| Accordion | `type`, `size`, `expand` | **`showLeadingIcon`**(+`└ leadingIcon` Instance Swap), **`showBodyTxt`**, **`showBadge`**, **`showTopDivider`**, **`showBottomDivider`**, **`showSubItems`**, Slot `addSubRow`, Slot `addSubAccordion` |
| Price | `type`, `size`, `currency`, `discout` | **`price`**, **`discountPrice`**, **`originalPrice`** (텍스트 프로퍼티) |
| OptionRow | `viewport`, `showOption`, `isDisabled` | **`isDiscount`**, **`optionName`** |
| ProductCard | `viewport` | **`showImageBadge`**, **`showBadge`**, **`showLabel`**, **`discount`**, **`textLines`**, **`currency`** |
| InfoCard | `viewport`, `isDiscount`, `isOverseas` | **`showStepper`**, **`showCoupon`** |
| ProfileCard | `size`, `state` | **`showAvatar`**, **`showSubtitle`** |
| CartItem *(Slot)* | — | Slot **`addOptionRow`** |

Accordion 은 베리언트 3개 뒤에 **boolean 6개 + Slot 2개**가 더 있습니다.
베리언트 목록만 보면 10개 중 3개만 알게 됩니다.

구현 시 props를 베리언트 목록만 보고 정의하면 이 항목들이 누락됩니다.

---

## 상세 페이지의 컴포넌트 11종

### Accordion `1621:13143`

| 프로퍼티 | 값 |
|---|---|
| `type` | `info` · `contents` |
| `size` | `lg` · `md` · `sm` |
| `expand` | `true` · `false` |

베리언트 12개 (2 × 3 × 2). 실측 높이 — `lg` 60 · `md` 52 · `sm` 44.

#### 사용 가이드 — `Accordion(Usage)` `4073:12234`

> **Guide** — Accordion 컴포넌트의 속성별 사용법을 안내합니다.

10개 절로 **속성 하나씩** 설명합니다. 이 파일에서 가장 촘촘한 가이드입니다.

| # | 절 | 시안 설명 (원문) |
|---|---|---|
| 1 | **Type** | type 속성으로 아코디언의 유형을 선택합니다. `info`는 펼쳤을 때 자유로운 콘텐츠를 Slot(InfoContainer)으로 삽입할 수 있고, `contents`는 하위 아이템 목록을 표시합니다. |
| 2 | **Size** | size 속성으로 아코디언의 높이를 조절합니다. lg · md · sm 세 가지 크기를 지원하며, 사용 맥락에 맞게 선택합니다. |
| 3 | **Expand** | expand 속성으로 아코디언의 펼침/접힘 상태를 전환합니다. false일 때 제목만 표시되고, true일 때 하위 콘텐츠가 노출됩니다. |
| 4 | **Show Leading Icon** | showLeadingIcon 속성을 활성화하면 제목 왼쪽에 아이콘이 표시됩니다. `└ leadingIcon` 속성(Instance Swap)으로 원하는 아이콘으로 교체할 수 있습니다. |
| 5 | **Show Body Text** | showBodyTxt 속성을 활성화하면 제목 아래에 부가 설명 텍스트가 표시됩니다. 접힌 상태에서도 추가 정보를 함께 노출할 수 있습니다. |
| 6 | **Show Badge** | showBadge 속성을 활성화하면 제목 옆에 Badge가 표시됩니다. 새로운 항목이나 업데이트된 항목을 강조할 때 사용합니다. |
| 7 | **Show Top / Bottom Divider** | showTopDivider, showBottomDivider 속성으로 상단·하단 구분선의 노출 여부를 개별 설정합니다. **여러 아코디언을 연속 배치할 때 중복 구분선을 방지**할 수 있습니다. |
| 8 | **Show Sub Items** | `└ showSubItems` 속성으로 contents 타입의 하위 아이템 목록 노출 여부를 설정합니다. expand=true 상태에서 적용되며, 비활성화하면 빈 컨테이너만 표시됩니다. |
| 9 | **addSubRow** (Slot) | addSubRow Slot을 사용하여 info 타입 아코디언의 펼친 영역에 자유 콘텐츠를 삽입할 수 있습니다. expand=true 상태에서 Slot 영역이 활성화됩니다. |
| 10 | **addSubAccordion** (Slot) | addSubAccordion Slot을 사용하여 아코디언 내부에 **중첩(Nested) 아코디언**을 삽입할 수 있습니다. contents 타입의 expand=true 상태에서 하위 아코디언을 구성할 때 활용합니다. |

`showTopDivider` / `showBottomDivider` 프리뷰는 `divider=both` · `top only` · `none` 세 가지를 보여줍니다.
구성 요소로 `New Badge`, `Sub Accordion`, `Info Row`(Label + Value)가 쓰입니다.

> **Figma Slot 기능**을 쓰는 유일한 컴포넌트입니다(`addSubRow`, `addSubAccordion`).
> 코드로는 children / render prop 에 대응합니다.

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

#### 사용 가이드 — `OptionRow(Usage)` `4726:13681`

> **Guide** — 옵션 행(OptionRow)의 사용 예시를 안내합니다.

| 절 | 시안 설명 (원문) |
|---|---|
| **Show Option** | 옵션 정보 노출 여부를 `showOption=true/false`로 설정합니다. |
| **Is Discount** | 할인 가격 노출 여부를 `isDiscount=true/false`로 설정합니다. |
| **Is Disabled** | 비활성 상태에 따라 `isDisabled=true/false`로 설정합니다. |
| **Option Name** | `optionName` 속성으로 옵션명을 설정합니다. |

실측값 — 폭 **335px 고정**, 높이 `showOption=true` **88** / `false` **56**.
`isDiscount=true` 는 원가에 취소선 + 할인율(예 `5%`, `color/text/status/negative`) + 할인가를 함께 보여줍니다.
`optionName` 프리뷰는 `default`(옵션 A) / `custom`(옵션 B) 두 가지입니다.

Figma 컴포넌트 설명(`3421:17455`):
> 상품 옵션명, 수량 조절(Stepper), 가격을 한 행으로 표시하는 공용 컴포넌트입니다.
> 장바구니, 상품 상세 등 옵션 선택이 필요한 다양한 맥락에서 사용됩니다.

> `[?]` 가이드에는 `viewport` 가 없고 대신 `isDiscount` 가 있습니다. 베리언트 목록과 축이 다릅니다.

### Price `3432:15991`

| 프로퍼티 | 값 |
|---|---|
| `type` | `info` · `product` · `cart` |
| `size` | `lg` · `md` |
| `currency` | `KRW` · `USD` · `JPY` |
| `discout` ※오타 | `true` · `false` |

베리언트 36개 (3 × 2 × 3 × 2). 프로퍼티 이름 `discout` 는 **Figma 원문 그대로의 오타**입니다(`discount`).

**다중 통화(KRW / USD / JPY)를 토큰 레벨이 아니라 컴포넌트 베리언트로 다룹니다.**

#### 사용 가이드 — `Price(Usage)` `4703:13314`

> **Guide** — 가격(Price)의 사용 예시를 안내합니다.

7개 절. 앞 4개는 베리언트, 뒤 3개는 **텍스트 프로퍼티**입니다.

| 절 | 시안 설명 (원문) |
|---|---|
| **Type** | 사용 맥락에 따라 info, product, cart 타입을 선택합니다. |
| **Size** | 화면 위계에 따라 lg, md 크기를 선택합니다. |
| **Currency** | 통화에 따라 KRW, USD, JPY를 선택합니다. |
| **Discout** ※오타 | `discout` 속성으로 할인 정보 표시 여부를 선택합니다. |
| **Price** | `price` 속성으로 판매가 숫자를 설정합니다. |
| **Discount Price** | `discountPrice` 속성으로 **할인율 텍스트**를 설정합니다. |
| **Original Price** | `originalPrice` 속성으로 **할인 전 가격 텍스트**를 설정합니다. |

Figma 컴포넌트 설명(`3436:8388`):
> 상품 가격을 표시하는 공통 아토믹 요소.
> **외화 전환 시 original price의 통화 기호를 변경해서 사용합니다.**
> 1. type: 사용 맥락에 따른 스타일 분기 (product / info / cart)
> 2. size: lg / md
> 3. currency: 통화 단위 (KRW / USD / JPY)
> 4. discout: 할인 여부 (true 시 할인율 + 원가 표시)

구성: `KRW`(통화 코드, `Caption/semibold/3` 10px) + `₩`(기호, 13px) + 숫자(14px).
절 제목과 프로퍼티 이름 모두 `Discout` 오타가 그대로 쓰입니다.

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

2026-10-15 에 **6개 절로 보강**됐습니다(1213 → 2571px).

| 절 | 시안 설명 (원문) |
|---|---|
| **Size** | 사용 맥락에 따라 `lg`, `md`, `sm`, `xs` 크기를 선택합니다. |
| **Color** | 정보 위계에 따라 `primary`, `secondary`, `tertiary` 색상을 사용합니다. |
| **Text Align** | 레이블의 정렬 방향을 `left`, `center`, `right` 중에서 선택합니다. |
| **Show Count** | 글자 수 정보가 필요할 때 `showCount` 를 사용합니다. **true 상태를 먼저 배치합니다.** |
| **Show Required** | 필수 입력 항목에는 `showRequired` 를 사용합니다. **true 상태를 먼저 배치합니다.** |
| **Text** | `label` 텍스트 속성으로 맥락에 맞는 명확한 이름을 제공합니다. |

필수 표시(`*`)는 `color/text/status/negative` 입니다. Change Log `260204` 의 `required` 항목과 이어집니다.

Figma 컴포넌트 설명(`225:1969`):
> 특정 개체에 대한 간략한 설명을 나태내는 요소 ※오타
> 1. 폼 필드, 데이터 항목 등에 사용합니다.
> 2. `textAlign` 사용 시, W는 fill로 사용합니다.

> `[?]` 가이드는 텍스트 속성을 **`label`** 이라 부르는데, 코드 출력에서는 **`text`** 로 나옵니다.
> `color` 축(primary/secondary/tertiary)도 베리언트 목록에는 없습니다.

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

`7712 × 9598`. 5종 카드를 각각 절로 나누고, 그 아래 프로퍼티별 하위 절을 둡니다.

##### Product Card
> 조합에 따라 다양한 형태의 속성이 존재합니다.

| 하위 절 | 시안 설명 (원문) |
|---|---|
| **Maximum Options** | 모든 옵션을 활성화했을 때의 최대 구성 예시입니다. 이미지 내 Badge · Wishlist 버튼, 브랜드명 · 상품명 · 할인 가격 · **상태 Badge(max 4개)** 가 동시 노출되며, 반응형 뷰포트에서 콘텐츠가 가장 많을 때에도 레이아웃이 안정적으로 유지되는지 확인할 수 있습니다. |
| **Viewport** | Desktop과 Mobile 뷰포트에 따라 카드 크기를 조정합니다. **Mobile viewport의 default width는 140px입니다.** |
| **Show Image Badge** | 이미지 위에 표시되는 Badge의 노출 여부를 설정합니다. |
| **Show Badge** | **가격 하단**에 표시되는 Badge의 노출 여부를 설정합니다. |
| **Show Label** | **브랜드명(Label)** 텍스트의 노출 여부를 설정합니다. |
| **Discount** | 할인 적용 시 할인율과 정가가 함께 표시됩니다. |
| **Text Lines** | 상품명을 최대 몇 줄까지 노출할지 설정합니다. `Text Lines - 2` 는 최대 두 줄까지 표시한 뒤 **말줄임(…)** 처리합니다. |
| **Currency** | 가격 앞에 표시되는 통화 기호를 설정합니다. **KRW(₩)·USD($)·JPY(¥)** 를 지원합니다. |

##### Information Card
> 이미지·가격·옵션 정보를 함께 제공하는 카드로, 다양한 프로퍼티가 존재합니다.

| 하위 절 | 시안 설명 (원문) |
|---|---|
| **Maximum Options** | 모든 옵션을 활성화했을 때의 최대 구성 예시입니다. 옵션 셀렉트 필드 · 쿠폰 배너 · 옵션 Row(수량/가격) · 배송 정보(국내/해외)가 모두 표시됩니다. |
| **Viewport** | Desktop와 Mobile 뷰포트에 따라 레이아웃이 달라집니다. ※오타(`Desktop와`) |
| **Discount** | 기본형(false)과 할인형(true) 타입을 제공합니다. |
| **Overseas** | 해외 배송 여부에 따라 배송 정보 영역이 달라집니다. |
| **Show Stepper** | 수량 조절 스테퍼의 노출 여부를 설정합니다. |
| **Show Coupon** | 쿠폰/혜택 배너의 노출 여부를 설정합니다. |

##### Profile Card
> 아바타와 타이틀·서브타이틀로 구성된 카드로, 크기와 상태 프로퍼티가 존재합니다.

| 하위 절 | 시안 설명 (원문) |
|---|---|
| **Size** | `lg` 와 `md` 두 가지 크기를 제공합니다. |
| **State** | `default` / `hover` / `pressed` / `disabled` 4가지 상태를 제공합니다. |
| **Show Avatar** | 아바타(프로필 이미지)의 노출 여부를 설정합니다. |
| **Show Subtitle** | 서브타이틀 텍스트의 노출 여부를 설정합니다. |

##### Event Card `3476:9796` / Cart Item `3476:10039`

아래 두 절 참조. Cart Item 에는 절이 둘 더 붙었습니다.

| 하위 절 | 시안 설명 (원문) |
|---|---|
| **Anatomy** (Cart Item) | 컴포넌트의 내부 구조를 나타냅니다. 각 영역은 독립적인 하위 컴포넌트로 구성됩니다. |
| **Slot: addOptionRow** (Cart Item) | 슬롯을 통해 옵션 행(OptionRow)을 유연하게 추가하거나 제거할 수 있습니다. **다중 옵션 상품에는 여러 행을 추가합니다.** |

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
| 9 | Usage 가이드가 **없는** 컴포넌트: Avatar · Carousel · List · Table · Text List |
| 11 | `OptionRow` 가이드의 축(`isDiscount`)과 베리언트 축(`viewport`)이 다름 |
| 12 | `Price` 의 `discout` 오타가 절 제목·프로퍼티·컴포넌트 설명 세 곳에 모두 존재 |
| 13 | Label 가이드의 `label` ↔ 코드의 `text`, 그리고 `color` 축이 베리언트에 없음 |
| 14 | Card(Usage) 각 절의 프리뷰 치수는 미조사 (Mobile 140px 외) |
| 10 | `Sphere(스피어)` 도메인 용어의 정의 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
