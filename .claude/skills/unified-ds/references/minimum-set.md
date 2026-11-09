# 최소 세트 42개와 승격 규칙

## 최소 세트 (Semantic, 42개)

시작은 이 42개다. 이 밖의 토큰은 **승격 5조건**을 통과해야 하고, 생성 전 사용자 확인을 받는다.

### bg — 20

| # | 토큰 | # | 토큰 |
|---|---|---|---|
| 1 | `bg/layer-default` | 11 | `bg/informative-solid` |
| 2 | `bg/layer-basement` | 12 | `bg/informative-weak` |
| 3 | `bg/layer-floating` | 13 | `bg/positive-solid` |
| 4 | `bg/layer-fill` | 14 | `bg/positive-weak` |
| 5 | `bg/state-hover` | 15 | `bg/warning-solid` |
| 6 | `bg/state-pressed` | 16 | `bg/warning-weak` |
| 7 | `bg/neutral-solid` | 17 | `bg/critical-solid` |
| 8 | `bg/neutral-weak` | 18 | `bg/critical-weak` |
| 9 | `bg/brand-solid` | 19 | `bg/disabled` |
| 10 | `bg/brand-weak` | 20 | `bg/overlay` |

### fg — 13

`fg/neutral` · `fg/neutral-subtle` · `fg/neutral-muted` · `fg/neutral-placeholder` · `fg/neutral-contrast` ·
`fg/disabled` · `fg/brand` · `fg/informative` · `fg/positive` · `fg/warning` · `fg/critical` ·
`fg/contrast` · `fg/warning-contrast`

### stroke — 9

`stroke/neutral` · `stroke/neutral-muted` · `stroke/neutral-strong` · `stroke/focus` · `stroke/brand` ·
`stroke/informative` · `stroke/positive` · `stroke/warning` · `stroke/critical`

### 세트 밖에서 처리하는 것

- **accent 27개** — ContentBadge 가 primitive 를 **컴포넌트 로컬**로 직접 참조한다. Semantic 으로 만들지 않는다.
- **톤별 pressed** — 별도 토큰 없이 `bg/state-hover` · `bg/state-pressed` 오버레이 레이어를 얹는다.

기계 판독용 목록: [`scripts/minimum_set.json`](../scripts/minimum_set.json).

## 승격 5조건

새 토큰은 다음을 **모두** 만족할 때만 만든다.

1. 서로 다른 컴포넌트 **두 곳 이상**에서 같은 의도로 쓰인다
2. 모드 간 값이 다르거나, 기존 토큰과 **다른 시점에 바뀔 이유**가 있다
3. 문법에 맞고 기존 토큰과 **의미가 겹치지 않는다**
4. Light · Dark 값이 모두 있고 **대비를 통과**한다(텍스트 4.5:1, 아이콘·테두리 3:1)
5. 코드가 **자동 생성**되어 바로 쓸 수 있다

하나라도 실패하면 반려하고, 실패한 조건 번호와 대안(기존 토큰 · 레시피 · 컴포넌트 로컬)을 결정 기록에 적는다.

## 계층 선택

| 쓰는 곳 | 계층 | 비고 |
|---|---|---|
| 한 컴포넌트만 | 컴포넌트 로컬 | 메인 컴포넌트 안에서 Semantic 바인딩, 없으면 primitive 허용. 화면 인스턴스에서는 금지 |
| 한 모듈 안에서 둘 이상 | Module 토큰 | `commerce/` · `messenger/` |
| Core 둘 이상 또는 모듈 둘 이상 | Semantic | |
| 브랜드마다 다름 | Brand 램프 | 단일 토큰 금지 |

조건 1을 통과하지 못해도 계층이 "컴포넌트 로컬"이면 반려가 아니라 **로컬 처리 안내**로 끝낸다.

## 승격 절차

1. 제안서(`templates/promotion-proposal.md`) 접수
2. 조건 1–5 판정 — 조건 3·4·5는 `scripts/lint.py --spec` 으로 기계 판정
3. 승인 / 반려 → 결정 기록(`templates/decision-record.md`)
4. 승인 시 SKILL.md 4.2 절차(최소 세트 밖이므로 **사용자 확인 후**)
5. Updates 에 **결정** 항목(비고에 결정 안건 번호), 승인 시 추가 항목이 별도로 1건 더
