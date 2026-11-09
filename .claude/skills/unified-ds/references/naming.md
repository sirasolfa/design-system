# 이름 문법 · 어휘표 · 플랫폼 변환표

## 색 토큰 문법

```
{property}/{tone}-{emphasis}-{state}
```

- 세그먼트는 **이 순서로만** 온다. 각 자리는 생략할 수 있지만 순서를 바꿀 수 없다.
  (`bg/disabled` = tone 만, `fg/contrast` = emphasis 만, `bg/state-hover` = tone + state)
- 슬래시는 property 뒤 한 번만. 나머지는 하이픈.
- Module 토큰은 앞에 모듈 접두사: `commerce/bg/brand-weak`, `messenger/fg/neutral-subtle`.

### 어휘표 (승인된 어휘만 사용)

| 자리 | 어휘 |
|---|---|
| property | `bg` · `fg` · `stroke` |
| tone | `layer` · `neutral` · `brand` · `informative` · `positive` · `warning` · `critical` · `disabled` · `overlay` · `state` |
| emphasis | `solid` · `weak` · `subtle` · `muted` · `placeholder` · `contrast` · `strong` |
| state | `hover` · `pressed` · `selected` |
| layer 수식어 | `default` · `basement` · `floating` · `fill` — **tone = `layer` 바로 뒤에서만** 허용 |
| stroke 전용 tone | `focus` — **property = `stroke` 일 때만** 허용 |

> layer 수식어(`bg/layer-default` · `layer-basement` · `layer-floating` · `layer-fill`)와
> `stroke/focus` 는 요청서의 최소 세트에 이미 들어 있지만 tone · emphasis 어휘표에는 없다.
> 최소 세트가 승인된 것으로 보고 위치를 제한해 어휘표에 포함한다. 다른 자리에는 쓸 수 없다.
>
> "4톤" = `informative` · `positive` · `warning` · `critical`.

### 금지

- 컴포넌트명이 든 토큰 (`bg/button-primary`, `fg/badge-…`) — 컴포넌트는 레시피로 조합한다
- 순서 위반 (`bg/solid-brand`, `fg/hover-neutral`)
- 미승인 어휘 (`bg/info-solid`, `fg/secondary`, `bg/surface-default`)
- **어휘 추가는 토큰이 아니라 별도 안건**이다. 새 어휘가 필요하면 결정 기록(`templates/decision-record.md`)으로 올리고 사용자 확인을 받는다.

## 비색상 토큰 문법

| 종류 | 형식 | 예 |
|---|---|---|
| 간격 스케일 | `spacing/{n}` | `spacing/4`, `spacing/16` |
| 간격 용도 | `space/{용도}` | `space/inset-md`, `space/stack-sm` |
| 라디우스 | `radius/{size}` | `radius/sm`, `radius/full` |
| 테두리 두께 | `border-width/{n}` | `border-width/1` |
| 글자 크기 | `font/size/{n}` | `font/size/14` |
| 글꼴 | `font/family/{role}` | `font/family/base`, `font/family/display` |
| 그림자 | `elevation/{level}` | `elevation/1` |
| 모션 시간 | `motion/duration/{n}` | `motion/duration/200` |
| 모션 이징 | `motion/easing/{name}` | `motion/easing/standard` |

`border-width/{n}` 은 요청서의 비색상 컬렉션 목록(Border Width)에서 온 형식이다.
`space/{용도}` 의 용도 어휘는 아직 정해지지 않았다 → 첫 사용 시 결정 안건.

## Brand 컬렉션 이름

```
brand/primary/{step}      step = 50 · 100 · 200 · 300 · 400 · 500 · 600 · 700 · 800 · 900 · 950  (11단계)
brand/secondary/{step}
font/family/{role}
```

단일 토큰(`brand/primary` 처럼 단계 없는 것)은 금지.

## 플랫폼 변환표

변환은 **결정적이며 자동**이다. 사람이 이름을 따로 짓지 않는다.

| Figma | tokens.json 경로 | CSS | TypeScript | Dart |
|---|---|---|---|---|
| `bg/neutral-solid` | `bg.neutral-solid` | `--bg-neutral-solid` | `tokens.bg.neutralSolid` | `context.tokens.bg.neutralSolid` |
| `fg/warning-contrast` | `fg.warning-contrast` | `--fg-warning-contrast` | `tokens.fg.warningContrast` | `context.tokens.fg.warningContrast` |
| `commerce/bg/brand-weak` | `commerce.bg.brand-weak` | `--commerce-bg-brand-weak` | `tokens.commerce.bgBrandWeak` | `context.tokens.commerce.bgBrandWeak` |
| `font/size/14` | `font.size.14` | `--font-size-14` | `tokens.font.size14` | `context.tokens.font.size14` |
| `motion/duration/200` | `motion.duration.200` | `--motion-duration-200` | `tokens.motion.duration200` | `context.tokens.motion.duration200` |
| `spacing/4` | `spacing.4` | `--spacing-4` | `tokens.spacing.n4` | `context.tokens.spacing.n4` |
| `radius/2xl` | `radius.2xl` | `--radius-2xl` | `tokens.radius.n2xl` | `context.tokens.radius.n2xl` |

규칙:

1. **tokens.json** — `/` 를 `.` 로 (DTCG 그룹 중첩). 하이픈은 그대로.
2. **CSS** — `/` 와 `.` 를 `-` 로, 앞에 `--`.
3. **TS · Dart 그룹** — 첫 세그먼트(`bg`, `fg`, `stroke`, `commerce`, `font`, `spacing` …).
4. **TS · Dart 키** — 나머지 세그먼트를 `-` 로 이어 camelCase.
5. 키가 숫자로 시작하면 앞에 `n` 을 붙인다(Dart 식별자 제약). TS 도 같은 키를 써서 두 플랫폼 이름을 맞춘다.

> 규칙 5(`n` 접두사)는 이 스킬이 정한 변환이며 요청서에 명시되지 않았다.
> 다른 접두사를 원하면 결정 안건으로 바꾸고 `scripts/naming.py` 한 곳만 고친다.

구현: [`scripts/naming.py`](../scripts/naming.py) — 모든 생성기와 린트가 이 함수 하나를 쓴다.
