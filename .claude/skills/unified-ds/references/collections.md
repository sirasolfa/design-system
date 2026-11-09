# 컬렉션 · 모드 · scope 스펙

## 컬렉션

| 컬렉션 | 모드 | 담는 것 | 값 | 공개 |
|---|---|---|---|---|
| **Primitive** | 없음(단일 모드) | 원시색 · 숫자 · 폰트명 | 리터럴 | `hiddenFromPublishing = true`. **화면 직접 사용 금지** |
| **Brand** | 서비스: `NOVERA` · `1CHON` | `brand/primary/*` · `brand/secondary/*` 램프 11단계, `font/family/*` | Primitive alias 또는 리터럴 | 공개 |
| **Semantic** | `Light` · `Dark` | bg · fg · stroke | **Primitive 또는 Brand alias 만.** hex 직접 입력 금지 | 공개 |
| **Module** | Semantic 과 같음(`Light` · `Dark`) | `commerce/*` · `messenger/*` | **Semantic alias 만.** 모듈 간 참조 금지 | 공개 |
| **Spacing** | 없음 | `spacing/*` · `space/*` | 숫자 / Spacing alias | 공개 |
| **Radius** | 없음 | `radius/*` | 숫자 | 공개 |
| **Border Width** | 없음 | `border-width/*` | 숫자 | 공개 |
| **Typography** | 스케일: `100` · `110` · `120` · `135` (%) | `font/size/*` (font-family 는 Brand) | 숫자 | 공개 |
| **Elevation** | `Light` · `Dark` [?] | `elevation/*` | 그림자 파라미터 | 공개 |
| **Motion** | `Default` · `Reduced` | `motion/duration/*` · `motion/easing/*` | 숫자 · 문자열 | 공개 |

- 서비스 추가 = Brand 컬렉션에 **모드 추가**(사용자 확인 필요). 컬렉션을 새로 만들지 않는다.
- Module 은 `Module · Commerce` · `Module · Messenger` 두 컬렉션으로 나누거나 하나로 두고 접두사로 구분한다.
  어느 쪽이든 **모듈 간 alias 금지**는 린트로 강제한다.
- Elevation 의 모드 유무는 요청서에 없다 → `[?]`. 처음 만들 때 결정 안건으로 올린다.
- Typography 스케일 모드 값 = `round(기준값 × 배율)`. 100% 모드가 기준.

## 모드 해석 문맥

코드 생성 시 각 컬렉션의 모드는 아래 축에서 고른다.

| 축 | 값 | 적용 컬렉션 |
|---|---|---|
| brand | NOVERA · 1CHON | Brand |
| theme | Light · Dark | Semantic · Module · (Elevation) |
| scale | 100 · 110 · 120 · 135 | Typography — 코드에서는 기본 100 만 내보내고 배율은 런타임(TextScaler / rem) |
| motion | Default · Reduced | Motion — 코드에서는 Default 를 내보내고 Reduced 는 런타임 분기 |

## scope

`ALL_SCOPES` 는 **금지**. 변수 생성 시 항상 명시한다.

| 이름 접두사 | scopes |
|---|---|
| `bg/` (Module 포함) | `FRAME_FILL` · `SHAPE_FILL` |
| `fg/` | `TEXT_FILL` · `SHAPE_FILL` · `STROKE_COLOR` |
| `stroke/` | `STROKE_COLOR` |
| `spacing/` · `space/` | `GAP` · `WIDTH_HEIGHT`(패딩은 Figma 에서 `GAP` scope 로 바인딩) |
| `radius/` | `CORNER_RADIUS` |
| `border-width/` | `STROKE_FLOAT` |
| `font/size/` | `FONT_SIZE` |
| `font/family/` | `FONT_FAMILY` |
| `motion/` · `elevation/` | `[]` (피커에 노출 안 함 — 코드 전용) |
| Primitive · Brand 램프 | `[]` (직접 바인딩 금지, alias 전용) |

> Figma API 의 실제 scope 이름은 `STROKE` 가 아니라 `STROKE_COLOR` 다. 요청서의 "STROKE" 는 이것으로 읽는다.
> 패딩 전용 scope 는 Figma 에 없다. 요청서의 "GAP과 패딩"은 `GAP` 하나로 처리한다.
> spacing 에 `WIDTH_HEIGHT` 를 넣을지는 `[?]` — 넣지 않는 것이 요청서 문구에 더 가깝다. 린트는 `GAP` 포함 여부만 검사한다.

## 생성 순서 (Figma)

1. Primitive → 2. Brand → 3. Semantic → 4. Module → 5. 비색상.
alias 는 대상이 먼저 있어야 걸 수 있다. 각 단계 뒤 개수와 모드 완성도를 반환해 확인한다.
