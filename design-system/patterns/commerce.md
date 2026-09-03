# Commerce 패턴 `[F]`

> 출처 — `Card(Usage)` `2582:8855`, `Action Area(Usage)`(Bottom Sheet `1065:18681`), `Search(Usage)` `1170:5163`
> 아래는 Usage 프레임의 **레이어 구성에서 읽어낸 조합**입니다. 픽셀 수치는 조사하지 않았습니다.

NDS는 커머스(NOVERA shop) 전용 개념을 컴포넌트 레벨에 직접 담고 있습니다:
상품 · 가격 · 통화 · 할인 · 해외배송/관세 · 옵션 · 장바구니 · 아티스트 · 이벤트.

---

## 1. 상품 카드 (ProductCard)

`Card(Usage)` 의 `Product Card` 블록 구성 — desktop / mobile 뷰포트를 나란히 제시합니다.

```
ProductCard (viewport=desktop | mobile)
├ Image Area
│  ├ Ratio                     ← Thumbnail 계열. ratio=1:1 | 1.618:1 | 16:9
│  ├ Image Background
│  └ Badge                     ← 상태/프로모션 뱃지
├ └ ProductWish-atomic         ← 찜(하트). size=lg|sm, selected=true|false
├ Bottom Container
│  ├ └ ProductTitle-atomic     ← size=lg|md, textLines=1|2
│  └ Price Area
│      └ └ Price               ← type=product, currency=KRW|USD|JPY, discout=true|false
└ BadgeContainer / └ count
```

`Product List` 는 위 카드를 나열한 목록 예시이고, `Currency Switcher` 로 통화 전환 예시를 함께 보여줍니다.

**통화는 Price 컴포넌트의 베리언트**(`currency=KRW | USD | JPY`)로 처리합니다. → [../components/content-display.md](../components/content-display.md#price-343215991)

## 2. 상품 상세 (InfoCard)

```
InfoCard (viewport, isDiscount, isOverseas)
├ Top Container
│  └ Artist Container          ← Avatar + Artist Text + Chevron Icon
├ Content Container
│  ├ Product Title / Product Description
│  ├ Discount Info             ← isDiscount=true 일 때
│  └ └ Price
├ Select Area
│  ├ SelectField
│  └ └ OptionRow               ← 옵션 선택 행
├ Shipping Select Area
│  ├ Shipping Info Container   ← └ Label + application/delivery 아이콘
│  └ Shipping Select Container
├ Accordion Container
│  ├ Product Information
│  └ Additional Product Information
└ ButtonActionBar              ← 하단 고정 액션
```

### 해외 배송 (`isOverseas=true`)

`isOverseas` 가 켜지면 아래 블록이 추가로 노출됩니다.

| 블록 | 구성 |
|---|---|
| `Weight Info Container` | `Weight Label` + `Weight Value` |
| `Calculation Info Container` | `suggested/info` 아이콘 + `Shipping Calculation Info` |
| `Shipping Fee Container` | `Shipping Fee Label` + `Shipping Fee Info` |
| `Import Duty Container` | `Import Duty Label` + `Import Duty Info` (관세) |

### 혜택 / 쿠폰 / 옵션 원자 컴포넌트

| 컴포넌트 | 프로퍼티 |
|---|---|
| `└ InfoBenefit-atomic` | `viewport`, `type=default \| benefit`, `expanded=true \| false` |
| `└ InfoOption-atomic` | `size=md \| sm`, `state=default \| hover \| disabled`, `selected=True \| False` |
| `└ InfoCoupon-atomic` | 베리언트 없음 |

## 3. 장바구니 (CartItem)

`Cart Item(Usage)` 와 바텀시트의 `Action Area(Usage)` 두 곳에 같은 조합이 나옵니다.

```
CartItem (viewport=desktop|mobile, state=default|selected|disabled)
├ └ Checkbox-atomic            ← 선택
├ Product Info
│  ├ Product Container
│  │  └ Ratio                  ← 썸네일
│  └ Product Details
│      ├ Product Name
│      └ Price Container
│          ├ Price Label
│          └ Price Details → Currency + Price Amount
├ addOptionRow / └ OptionRow   ← 옵션 추가·변경
└ IconOnly                     ← 삭제 등 아이콘 버튼
```

> **장바구니 화면에서 선택한 상품의 정보를 표시하는 카드입니다. 상품 이미지, 상품명, 가격,
> 수량 조절, 옵션 표시 등의 기능을 포함합니다.** — `Cart Item(Usage)` `3476:10039` 원문

| 프로퍼티 | 값 | 시안 설명 |
|---|---|---|
| `viewport` | `desktop` · `mobile` | Desktop과 Mobile 뷰포트에 따라 카드의 **레이아웃**이 변경됩니다. |
| `type` | `default` · `disabled` | 상품의 구매 가능 상태에 따라 Default와 Disabled 타입으로 구분됩니다. |
| `checked` | `true` · `false` | 체크박스를 통해 상품의 선택 상태를 나타냅니다. |

`disabled` = **품절**. 썸네일에 `Thumbnail` 의 `showDimmer`(SOLD OUT 딤)가 적용되고,
상품명·가격·옵션·수량 스테퍼가 흐려지며 체크박스가 비활성화됩니다.

옵션 행은 `옵션 <값>` + 우측 `×`(삭제), 그 아래 `− 1 +` 스테퍼와 `KRW ₩999,999` 가격이 놓입니다.

바텀시트 버전은 여기에 `ActionArea` + `ButtonPair` 가 붙습니다
(`Bottom Sheet` `1065:18681` 안의 `Action Area(Usage)`).

**즉 장바구니는 "화면"이 아니라 `BottomSheet` + `CartItem` + `ActionArea` 조합으로 정의돼 있습니다.**

### 액션 영역 (ActionArea)

> **버튼 배치 방향에 따라 Horizontal, Vertical 두 가지 레이아웃을 제공합니다.**

| 컴포넌트 | 시안 설명 | 사이즈 |
|---|---|---|
| `ButtonPair` | ActionArea 내부의 버튼 쌍으로, 사이즈와 방향 조합을 제공합니다. | `large` · `medium` · `small` (horizontal / vertical) |
| `ButtonActionBar` | 아이콘 버튼과 메인 버튼을 결합한 액션 바 형태입니다. | `large` · `medium` |
| `ActionArea` | `direction=horizontal \| vertical` | — |

`ButtonActionBar` 는 `하트(찜) + 장바구니 + 메인 버튼` 구성이며, 찜을 누른 상태(`Press Heart Button`)는
하트만 채워진 빨강으로 바뀝니다. 세로 배치에서는 **주 버튼이 위**로 올라갑니다.
→ [../components/overlay.md](../components/overlay.md)

## 4. 이벤트 카드 (EventCard)

> **Event Card는 Sphere(스피어)의 정보를 나타내는 카드로, 스피어 탭의 이벤트 내용을 나타내는 요소로 사용합니다.**
> — `Event Card(Usage)` `3476:9796` 원문

| 프로퍼티 | 값 | 시안 설명 |
|---|---|---|
| `viewport` | `desktop` · `mobile` | Desktop과 Mobile 뷰포트에 따라 카드 크기를 조정합니다. |
| `status` | `upcoming` · `ongoing` · `ended` | 이벤트의 상태(예정/진행 중/종료)에 따라 카드의 시각적 표현이 변경됩니다. |
| `showSubtitle` | `true` · `false` | 서브타이틀의 표시 여부를 설정합니다. |

상태별 표현:

| status | 배지 | 이미지 | 텍스트 |
|---|---|---|---|
| `upcoming` | **예정** (연한 배지) | 기본 | 기본 |
| `ongoing` | **진행중** (검정 배지) | 밝은 회색 | 날짜가 브랜드 컬러 |
| `ended` | **종료** | 어둡게 딤 | 전체 흐림 |

카드 구성: 이미지 + 상태 배지(좌상단) / 타이틀 / 서브타이틀(선택) / `editor/calendar` 아이콘 + 기간(`202Y.MM.DD — MM.DD`).

`showSubtitle` 은 베리언트 목록에 없는 boolean 프로퍼티입니다.
→ [../components/content-display.md](../components/content-display.md)

## 5. 프로필 카드 (ProfileCard)

`size=lg | md` × `state=default | hover | pressed | disabled`.
`└ ProfileWish-atomic`(`size`, `pressed`)로 팔로우/찜 인터랙션을 분리했습니다.
아티스트 프로필 표현에 쓰이는 것으로 보입니다 `[?]`(용도 명시 문구는 미조사).

## 6. 검색

`Search(Usage)` `1170:5163` — `1440 × 9388`. 절 구성은 **State · Spec · Behavior · With Keyboard** 입니다.
Overview 상 `Inputs > Search` 는 **Done** 상태입니다.
`[?]` 각 절의 상세 내용은 미조사입니다. → [../components/inputs.md](../components/inputs.md)

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | 각 Usage 프레임의 실제 치수(카드 폭, 갭, 패딩) — 레이어 구조만 조사함 |
| 2 | `Search(Usage)` 4개 절의 상세 내용 |
| 3 | 상품 상태(품절/재입고/한정) 표현 규칙 — `Badge` 가 Done이나 값 정의 미확인 |
| 4 | 통화 전환(`Currency Switcher`)의 동작 규칙 |
| 5 | `ProfileCard` 의 용도 — 가이드 설명은 "아바타와 타이틀·서브타이틀로 구성된 카드"까지만 |
| 6 | `Sphere(스피어)` 도메인 용어의 정의 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#patterns)
