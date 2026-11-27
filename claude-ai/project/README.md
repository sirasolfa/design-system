# NOVERA Design System

NDS(NOVERA Design System)는 NOVERA shop(커머스)의 UI를 만드는 디자인 시스템입니다.
원본은 Figma 파일 **NDS - NOVERA Design System**(`OJqTwQ8gHDGcvOOkOfYRgM`)이고,
이 디자인 시스템은 그 파일을 읽어 옮긴 문서 저장소 `sirasolfa/design-system`의 사실 문서로 만들었습니다.

[Figma 원본 열기](https://www.figma.com/design/OJqTwQ8gHDGcvOOkOfYRgM/NDS---NOVERA-Design-System?node-id=0-1)

> 서비스 명칭은 항상 **NOVERA shop**(shop 소문자)으로 씁니다. "NOVERA Shop"이라고 쓰지 않습니다.

---

## 먼저 읽을 것 — 신뢰 수준 표기

| 표기 | 뜻 | 다루는 법 |
|---|---|---|
| `[F]` | Figma에서 **직접 읽은 사실**. 토큰 값, 컴포넌트·베리언트 이름, 시안 문구. 노드 ID를 병기합니다. | 그대로 따릅니다. |
| `[?]` | Figma에 있지만 값을 못 읽었거나, **시안 안에서 값이 서로 어긋나는** 항목. | 추정하지 말고 사람에게 확인합니다. 각 섹션의 "확인 필요" 절에 모여 있습니다. |

이 디자인 시스템에는 `[F]`와 `[?]`만 들어 있습니다.
Figma에 근거가 없는 AI 제안(`[A]`, 원본 저장소의 `guidelines/ai-guidelines.md`)과
디자인팀 요청 목록(`guidelines/design-requests.md`)은 **넣지 않았습니다**. 채택 전 초안이기 때문입니다.

---

## 쓰는 규칙

1. **색은 semantic 토큰만** 씁니다. primitive 팔레트(`color/gray/*`, `color/blue/*` …)를 화면·컴포넌트에 직접 쓰지 않습니다.
2. **폰트 사이즈는 토큰이 아닙니다.** 텍스트 스타일(`Body/2`, `Title/3` …) 단위로 씁니다. 폰트는 **Pretendard Variable**.
   토큰화된 것은 font-family(`typo/font-family/primary`)와 weight(`typo/weight/regular` 400 · `semibold` 600 · `bold` 700)뿐입니다.
3. **gap은 요소 사이, spacing은 안팎 여백.** `layout/gap/*`는 카드 리스트·폼 필드 그룹·섹션 간 거리,
   `layout.spacing.*`는 버튼 padding·카드 내부 여백·섹션 상하 여백에 씁니다. 임의 숫자를 쓰지 않습니다.
4. **둥글기는 역할로 고릅니다.** 기본 버튼·입력·카드 `shape.rounded.sm`(8), 대형 카드 `md`(12),
   다이얼로그 `lg`(16), 바텀시트·드로워 `xl`(24), 칩·아바타 `full`.
5. **그림자는 4단계.** 리스트·헤더 `subtle`, 카드·인풋 기본 `default`, hover·focus·drag `raised`,
   모달·바텀시트·드롭다운 `overlay`. `raised`를 기본 상태에 상시 적용하지 않고, `overlay`를 일반 요소에 쓰지 않습니다.
6. **Grid 컬럼·거터·마진은 정해져 있지 않습니다**(MCP로 읽히지 않음). 추정해서 채우지 않습니다.
7. 다크 모드는 시안에 없습니다. 라이트 테마만 있습니다.

### 토큰 이름 읽는 법

정본 이름은 **Figma 변수 경로**(슬래시)입니다. 이 디자인 시스템의 tokens.json은 이름에 `/`를 쓸 수 없어
슬래시를 하이픈으로 바꿔 적었고, 각 토큰의 설명(usage) 맨 앞에 Figma 원래 이름을 붙였습니다.

| 이 시스템의 토큰 | Figma 변수 경로 | 문서 표 표기(별칭) |
|---|---|---|
| `color-text-primary` | `color/text/primary` | `color.text.priamry` ※오타 |
| `color-bg-surface-default` | `color/bg/surface/default` | `color.bg.default` |
| `layout-gap-16` | `layout/gap/16` | `layout.gap/16` |
| `layout-spacing-xs` | (변수 경로 미확인) | `layout.spacing.xs` |
| `shape-rounded-sm` | (변수 경로 미확인) | `shape.rounded.sm` |
| `elevation-shadow-default` | 스타일 `Semantic/Shadow/Default` | `Elevation.shadow.default` |

코드나 Figma 작업에서 이름을 쓸 때는 **가운데 열(Figma 변수 경로)** 을 씁니다.
점 표기와 슬래시 경로는 1:1이 아닐 수 있습니다(`color.bg.default` ↔ `color/bg/surface/default`).
텍스트 스타일도 같습니다: `Body-2` → Figma `Body/2`.

---

## 기초 요약 `[F]`

### 색

| 역할 | 토큰 (Figma) | 값 |
|---|---|---|
| 제목·가장 중요한 텍스트 | `color/text/primary` | `#171c24` |
| 본문 기본 | `color/text/secondary` | `#4b5465` |
| 보조 설명·메타 | `color/text/tertiary` | `#888e9c` |
| 플레이스홀더·캡션 | `color/text/muted` | `#a6acb7` |
| 링크 | `color/text/status/link` | `#355fea` |
| 기본 테두리 | `color/border/default` | `#edf0f5` |
| 기본 배경 | `color/bg/surface/default` | `#ffffff` |
| 보조 배경 | `color/bg/surface/subtle` | `#f9fafd` |
| 반전 배경 | `color/bg/inverse` | `#2f3744` |
| 브랜드 | `brand/default` | `#4f7cff` (= `color/blue/600`) |

primitive 팔레트는 gray 12단계(유일하게 `150` 단계가 있음)와 pink·red·yellow·green·cyan·blue·indigo 각 11단계,
그리고 base(black·white)와 alpha(black/white 8·16·24·40·64·80%)입니다.

### 텍스트 스타일

Display 2 · Title 5 · Subtitle 3 · Body 4(**기본값**) · Action 3(+underline 3, 버튼용) · Label 4 · Caption · Price.
행간은 배수(1.2–1.5), 자간은 px(−1 / 0 / 1)입니다.

### 간격

- `layout/gap/*`: 0 · 2 · 4 · 6 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 72 · 80 (이름 = px)
- `layout.spacing.*`: 6xs 2 · 5xs 4 · 4xs 6 · 3xs 8 · 2xs 12 · xs 16 · md 20 · lg 24 · xl 28 · 2xl 32 · 3xl 40 · 4xl 48 · 5xl 64 (`sm` 없음)

### 브레이크포인트

Desktop 1200px 이상 · Tablet 768–1199px · Mobile 375px 이하. 컴포넌트는 `viewport=desktop | mobile` 베리언트로 대응합니다(tablet 전용 베리언트 없음).

---

## 아직 정해지지 않은 것 `[?]`

아래는 사람이 정해야 합니다. 작업 중 이 값에 닿으면 추정하지 말고 확인을 요청하세요.

| 항목 | 상태 |
|---|---|
| `layout.spacing.xl / 2xl / 3xl` | 변수값 28/32/40, 시안에 인쇄된 라벨 32/40/48. 이 시스템은 변수값을 적었습니다. |
| `color/border/strong` ↔ `color/border/disabled` | 문서 표와 변수값의 매핑이 뒤바뀜. 이 시스템은 변수값(strong=gray/400, disabled=gray/300)을 적었습니다. |
| `color.icon.*` 실제값 | 변수값 미확인. 문서 표의 매핑만 적었습니다. |
| `Caption/1`, `Caption/3`, `Caption/semibold/2` | 값 미확인이라 넣지 않았습니다. |
| Grid 컬럼·거터·마진, 376–767px 구간 | 정의 없음. |
| 오타 토큰 `priamry`, `defualt`, `sementic` 등 | Figma 원문 그대로. 정정 여부 미정. |
| 로고 최소 크기·여백 규정 | 시안에 없음. |

---

## 섹션 안내

| 섹션 | 내용 |
|---|---|
| Foundations | 색 · 타이포그래피 · 레이아웃 · 모양 · 그림자 · 아이콘 · 브랜드(로고·파비콘·OG) |
| Components (인벤토리) | Overview 페이지의 50개 컴포넌트와 상태 |
| Components (카테고리별) | Button · Inputs · Navigation · Content Display · Overlay · Indicator & Status |
| Patterns | `(Usage)` 가이드 구성과 커머스 패턴(상품 카드 · 장바구니 · 이벤트 카드 · 검색) |
| Guidelines | 네이밍 규칙 · Change Log 원문 |

섹션 안의 Figma 노드 ID는 조회 시점의 스냅샷입니다. 노드 ID와 프레임 이름이 자주 바뀌므로, 작업 전 Figma에서 현재 상태를 다시 확인하세요.

이 디자인 시스템은 문서만 담습니다. 코드 컴포넌트 라이브러리와 폰트 파일은 들어 있지 않습니다.
Pretendard Variable은 쓰는 쪽에서 불러와야 합니다.
