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
| `Card(Usage)` | `2582:8855` | 7712×9511 | Product Card · Information Card · Profile Card · Event Card · Cart Item |
| ├ `Event Card(Usage)` | `3476:9796` | 1440×1946 | Viewport · Status · Show Subtitle |
| └ `Cart Item(Usage)` | `3476:10039` | 1440×2652 | Viewport · Type · Checked |
| `Thumbnail(Usage)` | `2980:8714` | 1440×2020 | Color · Ratio · Show Dimmer |
| `Label(Usage)` | `1621:17816` | 1440×1213 | Text Align · Show Count |
| `Drawer(Usage)` | `1358:8391` | 1440×2296 | Anatomy · Spec |
| `Toast(Usage)` | `1368:10031` | 1280×6008 | Element Patterns & Types · Behavior · Usage · Design Spec |
| `Action Area(Usage)` | `3572:31464` · `3261:4202` | 1440×1870 / 2791 | Button Pair · Button Action Bar · Action Area |
| `Search(Usage)` | `1170:5163` | 1440×9388 | State · Spec · Behavior · With Keyboard |

**Usage 가이드가 없는 컴포넌트** — Accordion · Avatar · Carousel · OptionRow · Price · List ·
Table · Text List · Dialog · Tooltip · Snack Bar. 이 컴포넌트들은 베리언트 목록만 있고
사용 규칙 문장이 없습니다.

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
| 1 | `Search(Usage)` (1440×9388) 의 내부 흐름은 이번 조사에서 구조만 확인. 단계별 화면 미조사 |
| 2 | 패턴 레벨의 문서(빈 상태·에러·로딩 처리 규칙)는 시안에 없음 |
| 3 | `Typography(Usage)` 의 각 레벨별 "언제 쓰는가" 설명은 예시 문구로만 제시되고 규칙 문장은 없음 |
| 4 | Toast 가이드 3개 절의 Description 이 비어 있음 |
| 5 | `Action Area(Usage)` 가 두 벌 존재 (`3572:31464` / `3261:4202`) |
| 6 | Usage 가이드가 없는 컴포넌트 11종의 사용 규칙 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#patterns)
