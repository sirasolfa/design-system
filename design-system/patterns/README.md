# Patterns `[F]`

NDS는 "패턴"이라는 이름의 별도 페이지를 두지 않습니다. 대신 컴포넌트 프레임 **하단에**
**`<이름>(Usage)`** 프레임을 두고, 거기에 **프로퍼티별 사용 규칙과 조합 예시**를 적습니다.
이 디렉터리는 그 `(Usage)` 프레임들을 정리한 것입니다.

> **중요** — Usage 가이드의 설명 문장은 **레이어 이름에 없습니다.** `get_metadata` 로는
> `Guide` · `Section Title` · `Description` 같은 껍데기 이름만 보이고, 실제 문구는
> `get_screenshot` 이나 `get_design_context` 로만 읽힙니다. 파운데이션 문서 다수를
> 레이어 이름에서 복원했던 것과 달리, 컴포넌트 사용 규칙은 이 경로로만 얻을 수 있습니다.

## 파일 안의 `(Usage)` 프레임 전체

| Usage 프레임 | 노드 | 크기 | 절 구성 |
|---|---|---|---|
| `Typography(Usage)` | `163:998` | 1600×7380 | Display · Title · Heading · Body · Action · Label · Caption |
| `Card(Usage)` | `2582:8855` | 7712×9598 | Product Card(8절) · Information Card(6절) · Profile Card(4절) · Event Card(3절) · Cart Item(5절) |
| ├ `Event Card(Usage)` | `3476:9796` | 1440×1946 | Viewport · Status · Show Subtitle |
| └ `Cart Item(Usage)` | `3476:10039` | 1440×2652 | Viewport · Type · Checked |
| `Thumbnail(Usage)` | `2980:8714` | 1440×2020 | Color · Ratio · Show Dimmer |
| `Accordion(Usage)` | `4073:12234` | 1613×5177 | 속성 10개를 한 절씩 (Slot 2종 포함) |
| `Price(Usage)` | `4703:13314` | 1602×2710 | Type · Size · Currency · Discout · Price · Discount Price · Original Price |
| `OptionRow(Usage)` | `4726:13681` | 1310×— | Show Option · Is Discount · Is Disabled · Option Name |
| `Dialog(Usage)` | `4805:36820` | 1440×1400 | height (최대 높이 80%) |
| `Label(Usage)` | `1621:17816` | 1440×2571 | Size · Color · Text Align · Show Count · Show Required · Text |
| `Drawer(Usage)` | `1358:8391` | 1440×2296 | Anatomy · Spec |
| `Toast(Usage)` | `4493:25180` | 1440×5193 | Overview · Spec(Anatomy·Variants·Show Icon·Show Close·Position·Interaction) · Usage(Do/Don't — 문구 작성 규칙) |
| `Sheet(Usage)` | `3572:31464` | 1440×1637 | Button Pair · Button Action Bar · Action Area<br>*(이전 이름 `Action Area(Usage)`)* |
| `BottomSheet(Usage)` | `1170:5163` | 1600×9388 | State · Spec · Behavior · With Keyboard<br>*(이전 이름 `Search(Usage)` — 2026-10-15 개명)* |

**Usage 가이드가 없는 컴포넌트** — Avatar · Carousel · List · Table · Text List · Tooltip ·
Snack Bar, 그리고 **Inputs 카테고리 13종 전부**.

> ⚠️ **노드 ID와 프레임 이름이 자주 바뀝니다.** 조사 몇 주 사이에 `Action Area(Usage)` → `Sheet(Usage)`
> 개명, `Dialog(Usage)` · `Accordion(Usage)` · `Price(Usage)` · `OptionRow(Usage)` 신설,
> Toast 프레임 비워짐이 일어났습니다. 이 표는 **2026-10-15 기준 스냅샷**입니다.

> ⚠️ **가이드를 식별할 때는 프레임 이름이 아니라 Title Container 의 Guide/Subtitle 텍스트를 확인하세요.**
> `Search(Usage)` 가 실제로는 Bottom Sheet 가이드였던 사례가 있었습니다(2026-10-15 개명 완료).

## Usage 프레임의 공통 구성 `[F]`

```
<이름>(Usage)
├ Title Container
│   ├ Guide                    ← "Guide" (Display/1, 56px)
│   └ Subtitle                 ← "<한글명>(<영문명>)의 사용 예시를 안내합니다."
└ Content
    └ Container                ← 프로퍼티/주제 단위
        ├ Title Container
        │   ├ Section Title    ← 프로퍼티명 (예: "Show Dimmer")
        │   └ Description      ← 규칙 문장 (비어 있는 경우도 있음)
        └ Section
            └ Text Sample
                ├ Container → Label + Design Only/Viewport   ← 하위 항목명 + Desktop/Mobile 칩
                └ Preview → Design Only/Value + 실제 인스턴스 ← 값 라벨 + 렌더
```

- **Guide/Subtitle 문구는 컴포넌트마다 같은 틀**입니다: `<한글명>(<영문명>)의 사용 예시를 안내합니다.`
- `Design Only/Viewport` 칩은 그 규칙이 적용되는 뷰포트(`Desktop` / `Mobile` / `Desktop / Mobile`)를 뜻합니다.
- `Design Only/Value` 칩은 프리뷰에 쓰인 프로퍼티 값(`large`, `showDimmer true` 등)입니다.

`Design Only/*` 는 Foundation 페이지의 `System Conponent` 섹션(`260:1443`)에 정의된 **문서 전용 부품**이며,
제품 UI가 아닙니다. 코드로 옮기지 않습니다.

## 문서

- [commerce.md](commerce.md) — 상품 카드 · 상품 상세 · 장바구니 · 이벤트 카드 · 검색

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | ~~`Search(Usage)` 프레임명 불일치~~ → **개명 완료**. 단 아직 페이지 최상위에 있어 이동 권장 |
| 2 | 패턴 레벨의 문서(빈 상태·에러·로딩 처리 규칙)는 시안에 없음 |
| 3 | `Typography(Usage)` 의 각 레벨별 "언제 쓰는가" 설명은 예시 문구로만 제시되고 규칙 문장은 없음 |
| 4 | Toast `Usage` 절의 Do / Don't 예시 문구 미조사 |
| 5 | `Action Area(Usage)` 가 두 벌 존재 (`3572:31464` / `3261:4202`) |
| 6 | Usage 가이드가 없는 컴포넌트 11종의 사용 규칙 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#patterns)
