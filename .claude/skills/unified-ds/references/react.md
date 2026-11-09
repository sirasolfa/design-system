# React 생성 규칙

## 출력

| 파일 | 내용 |
|---|---|
| `tokens.css` | Brand × Light/Dark **4조합**을 `[data-brand][data-theme]` 선택자의 CSS 변수로. `:root` = NOVERA · Light |
| `tokens.ts` | 타입이 있는 토큰 객체. 값은 `var(--…)` 참조라 런타임 테마 전환을 따른다 |

```css
:root, [data-brand="novera"][data-theme="light"] { --bg-neutral-solid: #1A1A1AFF; … }
[data-brand="novera"][data-theme="dark"]          { --bg-neutral-solid: #F5F5F5FF; … }
[data-brand="1chon"][data-theme="light"]          { … }
[data-brand="1chon"][data-theme="dark"]           { … }
```

```ts
import { tokens } from '@unified-ds/tokens';
<div style={{ background: tokens.bg.neutralSolid, color: tokens.fg.neutralContrast }} />
// <html data-brand="1chon" data-theme="dark"> 로 전환
```

## 파이프라인

```bash
python3 scripts/to_dtcg.py build/raw-variables.json -o tokens.json --version 1.3.0
python3 scripts/resolve_tokens.py tokens.json -o build/resolved
node scripts/style-dictionary.config.mjs build/resolved dist/react
```

- 해석본은 공개 토큰만 담는다(Primitive 는 hidden 이라 빠짐).
- 값 변환: dimension → `px`, duration → `ms`, fontFamily → 따옴표 문자열, 색은 `#RRGGBBAA` 그대로.
- Typography 스케일 모드: CSS 는 100% 값을 내보내고, 배율은 사용자 글자 크기 설정(`rem` 기반 루트 폰트)으로 처리 `[?]`.
- Motion Reduced: `@media (prefers-reduced-motion: reduce)` 블록에서 `--motion-duration-*` 를 Reduced 모드 값으로 덮어쓴다 `[?]` — 현재 생성기는 Default 만 낸다. Motion 컬렉션이 생기면 추가.

## 린트

- 컴포넌트 코드(`.ts` · `.tsx` · `.jsx`)의 **hex · px 리터럴은 실패**(`lint.py --src`).
- 생성 파일(`tokens.css` · `tokens.ts`)은 수정 금지. 값이 틀리면 Figma 변수 수정을 요청한다.
- 패리티: CSS 변수 수 = tokens.json 공개 토큰 수 = Figma 공개 변수 수.

## 선택 사항

Tailwind 프리셋 — `theme.extend.colors` 를 `tokens.ts` 에서 만들면 된다(값이 `var(--…)` 라 테마 전환 유지).
필요해질 때 생성기를 추가한다.

## 컴포넌트

props 이름 · 값 = Figma 변형 이름 · 값. [recipes.md](recipes.md) 의 스텁을 쓴다.
