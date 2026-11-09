# 컴포넌트 속성 모델과 조합 레시피

## 원칙

- **Figma 변형 속성 이름 · 값 = React props = Flutter 생성자 인자.** 대소문자·하이픈까지 같다.
  (Flutter 는 enum 값으로: `hierarchy: ButtonHierarchy.primary`)
- 컴포넌트 **전용 토큰을 만들지 않는다.** Semantic 토큰을 조합한 레시피로 만든다.
- hover · pressed 는 톤별 토큰 없이 `bg/state-hover` · `bg/state-pressed` 를 **위에 얹는 레이어**로 처리한다.
- 이름: Figma `Button` · React `<Button>` · Flutter `AppButton` (Flutter 는 `App` 접두사로 Material 과 충돌 회피).

## Button

| 속성 | 값 |
|---|---|
| `hierarchy` | `primary` · `assistive` · `brand` · `destructive` |
| `variant` | `solid` · `outlined` · `ghost` · `text` |
| `size` | `xl` · `lg` · `md` · `sm` · `xs` |
| `state` | `enabled` · `hover` · `pressed` · `disabled` (+ `loading`) |

`loading` 은 state 값이 아니라 boolean 프로퍼티로 둔다(`loading: true` 일 때 state 는 그대로 유지)… 라는 해석과
state 의 다섯 번째 값으로 두는 해석이 모두 가능하다 → **`[?]` 첫 통합 때 확정**. 요청서 표기는 "state(+loading)".

### solid 레시피 (요청서 확정)

| hierarchy | bg | fg |
|---|---|---|
| primary | `bg/neutral-solid` | `fg/neutral-contrast` |
| assistive | `bg/neutral-weak` | `fg/neutral-subtle` |
| brand | `bg/brand-solid` | `fg/contrast` |
| destructive | `bg/critical-solid` | `fg/contrast` |

| state | 처리 |
|---|---|
| hover | 위 + `bg/state-hover` 레이어 |
| pressed | 위 + `bg/state-pressed` 레이어 |
| disabled | `bg/disabled` + `fg/disabled` |

### outlined · ghost · text — 초안 `[?]`

요청서는 solid 만 정의한다. 아래는 같은 토큰으로 조합한 **초안**이며, 첫 Button 통합 작업에서 사용자 확인 후 확정한다.

| variant | bg | stroke | fg |
|---|---|---|---|
| outlined | 없음 | `stroke/{tone}` (primary·assistive → `stroke/neutral`) | solid 의 bg 톤 fg (`fg/neutral` · `fg/neutral-subtle` · `fg/brand` · `fg/critical`) |
| ghost | 없음 | 없음 | outlined 와 같음 |
| text | 없음 · 패딩 없음 | 없음 | outlined 와 같음 |

## Badge

| 속성 | 값 |
|---|---|
| `tone` | `neutral` · `brand` · `informative` · `positive` · `warning` · `critical` (6) |
| `variant` | `solid` · `weak` · `outline` |
| `size` | `[?]` 값 목록 미정 — 첫 통합 때 NDS·1CHON 의 기존 사이즈를 감사해 확정 |

| variant | bg | stroke | fg |
|---|---|---|---|
| solid | `bg/{tone}-solid` | — | `fg/contrast` |
| weak | `bg/{tone}-weak` | — | `fg/{tone}` |
| outline | — | `stroke/{tone}` | `fg/{tone}` |

예외:

- **neutral** 은 `fg/neutral` 대신 `fg/neutral-subtle` 을 쓴다(weak · outline).
- **warning solid** 는 `fg/warning-contrast` 를 쓴다 — 최소 세트에 이 토큰이 따로 있는 이유가
  노랑 계열 solid 위 흰 글자 대비 부족이라고 해석했다. 대비 린트가 `fg/contrast` 로 통과하면 그쪽을 쓴다 `[?]`.

> Badge(시스템 상태)와 ContentBadge(콘텐츠 분류, accent 27색)는 다른 컴포넌트다.
> ContentBadge 는 primitive 를 컴포넌트 로컬로 참조한다.

## 대비 검사 대상 (lint.py 가 읽는 표)

모든 brand × theme 조합에서 검사한다. bg 가 반투명이면 `bg/layer-default` 위에 합성한 뒤 계산한다.

| fg | bg | 기준 |
|---|---|---|
| `fg/neutral-contrast` | `bg/neutral-solid` | 4.5 |
| `fg/neutral-subtle` | `bg/neutral-weak` | 4.5 |
| `fg/contrast` | `bg/brand-solid` · `bg/critical-solid` · `bg/informative-solid` · `bg/positive-solid` | 4.5 |
| `fg/warning-contrast` | `bg/warning-solid` | 4.5 |
| `fg/{tone}` | `bg/{tone}-weak` (4톤 + brand) | 4.5 |
| `fg/neutral` · `fg/neutral-subtle` · `fg/neutral-muted` | `bg/layer-default` | 4.5 |
| `stroke/{tone}` · `stroke/neutral-strong` · `stroke/focus` | `bg/layer-default` | 3.0 |

`fg/disabled` · `fg/neutral-placeholder` · `stroke/neutral` · `stroke/neutral-muted` 는 WCAG 예외(비활성 · 장식)로 검사하지 않는다.

구현: [`scripts/contrast_pairs.json`](../scripts/contrast_pairs.json).

## Code Connect · props 스텁

컴포넌트 통합 시 함께 낸다.

```tsx
// React — 생성 스텁. props 이름·값은 Figma 변형과 동일
export type ButtonProps = {
  hierarchy?: 'primary' | 'assistive' | 'brand' | 'destructive';
  variant?: 'solid' | 'outlined' | 'ghost' | 'text';
  size?: 'xl' | 'lg' | 'md' | 'sm' | 'xs';
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
};
```

```dart
// Flutter — 생성 스텁
enum ButtonHierarchy { primary, assistive, brand, destructive }
enum ButtonVariant { solid, outlined, ghost, text }
enum ButtonSize { xl, lg, md, sm, xs }

class AppButton extends StatelessWidget {
  const AppButton({super.key, this.hierarchy = ButtonHierarchy.primary,
    this.variant = ButtonVariant.solid, this.size = ButtonSize.md,
    this.loading = false, this.onPressed, required this.child});
  // ...
}
```

state(hover · pressed · disabled)는 코드에서 상호작용으로 결정되므로 props 로 노출하지 않고,
`disabled` 는 React 의 `disabled` · Flutter 의 `onPressed == null` 로 대응한다.
Code Connect 매핑은 `figma-code-connect` 스킬을 따른다.
