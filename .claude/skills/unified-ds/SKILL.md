---
name: unified-ds
description: 노베라(NDS, 커머스)와 일촌(1CHON, 메신저·커뮤니티) 통합 디자인 시스템 작업 스킬. Primitive → Brand → Semantic 3계층 토큰, Core / Commerce / Messenger 라이브러리 구조로 Figma 변수·컴포넌트와 React·Flutter 토큰 코드를 같은 소스에서 생성·검증하고, 모든 변경을 Updates · Changelog 와 Progress Board 에 기록한다. "토큰 만들어줘", "변수 컬렉션 생성", "토큰 코드 내보내기", "컴포넌트 통합", "토큰 승격 검토", "디자인 시스템 감사", "진행 현황 갱신", "변경 이력 기록" 같은 요청이나, 통합 DS 파일(LjbepWOlFfYojApNoE2Fcg)·NDS·1CHON 파일의 변수·컴포넌트를 다룰 때 사용한다.
---

# unified-ds — 통합 디자인 시스템 운영 스킬

## 1. 개요

- **목적** — NDS(커머스)와 1CHON(메신저·커뮤니티)의 디자인 시스템을 하나로 통합·운영한다.
  Primitive → Brand → Semantic 3계층 토큰과 Core / Commerce / Messenger 라이브러리 구조를 기준으로,
  같은 소스에서 Figma 변수·컴포넌트와 React·Flutter 토큰 코드를 생성·검증하고,
  모든 변경을 **Updates · Changelog** 와 **Progress Board** 에 기록한다.
- **사용자** — 디자이너(Figma 변수·컴포넌트·문서), React 개발자(CSS 변수 + TS 토큰),
  Flutter 개발자(ThemeExtension Dart 토큰). 세 부류가 **같은 이름과 같은 기록**을 본다.
- **단일 소스** — 편집 소스는 **Figma Variables 하나**다.
  스킬이 `tokens.json`(W3C DTCG)을 추출하고 그로부터 코드를 생성한다.
  `tokens.json` 과 생성 코드는 **손으로 고치지 않으며**, 토큰 추가는 Figma 에서만 한다.
  변경 이력의 원본은 **Updates 페이지**이고, 코드 저장소의 `CHANGELOG.md` 는 거기서 생성한다.

## 2. 작업 전에 읽을 것

| 파일 | 언제 |
|---|---|
| [references/assets.md](references/assets.md) | **항상 먼저.** 파일 키·페이지·템플릿 컴포넌트·프로퍼티 이름, 현재 상태 스냅샷 |
| [references/naming.md](references/naming.md) | 토큰 이름을 만들거나 검사할 때 |
| [references/collections.md](references/collections.md) | 컬렉션·모드·scope 를 만들거나 검사할 때 |
| [references/minimum-set.md](references/minimum-set.md) | 토큰 생성·승격 검토 |
| [references/recipes.md](references/recipes.md) | 컴포넌트 통합, 대비 검사 |
| [references/react.md](references/react.md) · [references/flutter.md](references/flutter.md) | 코드 내보내기 |
| [references/logging.md](references/logging.md) | **모든 쓰기 작업의 마지막 단계** |

Figma 쓰기 전에는 반드시 `figma-use` 스킬을 로드하고(`skillNames` 에 포함),
라이브러리 자산(변수 컬렉션·컴포넌트 세트)을 만들 때는 `figma-generate-library` 도 함께 로드한다.
`create_session` 은 파일 키를 알게 되는 즉시 1회 호출하고 세션 ID 를 재사용한다.

## 3. 공통 골격

```
읽기 → 검증 → 쓰기 → 검증 → 기록
```

1. **읽기** — 대상 파일의 현재 상태를 읽는다. 노드 ID 는 스냅샷이므로 **이름으로 다시 찾는다**
   (`assets.md` 의 ID 는 초기값일 뿐, 하드코딩 금지).
2. **검증(사전)** — 입력 스펙을 `scripts/lint.py` 규칙(이름·참조·scope)에 대조한다. 실패하면 쓰지 않는다.
3. **쓰기** — `figma-use` 규칙을 따른다. 템플릿 컴포넌트의 프로퍼티 키(`날짜#37:0` 등)는
   **매번 이름으로 조회**한다(`#` 뒤 ID 는 바뀔 수 있음).
4. **검증(사후)** — 아래 [검증 체크리스트](#6-검증-체크리스트)를 자동 실행한다.
5. **기록** — Updates 항목 1건 + Progress Board 행 갱신. **기록 단계 없이 끝내면 작업 실패**다.
   감사(읽기 전용)만 예외.

## 4. 작업 유형별 절차

### 4.1 감사 (읽기 전용)

1. 통합 DS · NDS · 1CHON 파일의 컬렉션 · 스타일 · 컴포넌트를 읽는다(`scripts/figma/extract-variables.js`, 페이지별 컴포넌트 목록).
2. 매트릭스(토큰/컴포넌트 × 파일)와 diff 리포트를 만든다.
3. `scripts/lint.py` 를 추출본에 돌려 규칙 위반을 붙인다.
4. **기록 누락**을 함께 낸다: Updates 에 없는 변수 diff, 수정자가 빈 항목, 영향 행 갱신일 불일치
   (`scripts/figma/read-updates.js` + `scripts/audit_log.py`).
5. 쓰기와 기록은 하지 않는다. 리포트만 낸다.

### 4.2 토큰 생성 · 변경

1. 스펙 JSON 검증(`lint.py --spec`) — 이름 문법, 계층, alias 대상, scope.
2. 컬렉션 · 모드 생성(없을 때만, [collections.md](references/collections.md)).
3. 변수 생성 — scope · alias · `hiddenFromPublishing` 지정.
4. 개수와 모드 완성도 확인.
5. 컬러칩 문서 프레임 갱신(`templates/color-chip-frame.md`).
6. Updates 항목 → Progress Board 행.

### 4.3 코드 내보내기

1. Figma → `tokens.json` (`scripts/figma/extract-variables.js` → `scripts/to_dtcg.py`)
2. `tokens.json` → 브랜드×테마 해석본 (`scripts/resolve_tokens.py`)
3. Style Dictionary → React CSS · TS (`scripts/style-dictionary.config.mjs`)
4. Dart 생성 (`scripts/gen_dart.py`)
5. 검증 (`scripts/lint.py --tokens ... --css ... --dart ...` — 패리티 포함)
6. Updates **릴리스** 항목 → Progress Board 의 React · Flutter 열 갱신
7. `CHANGELOG.md` 생성 (`scripts/changelog.py`)

### 4.4 컴포넌트 통합

1. 속성 모델 확정([recipes.md](references/recipes.md)) — Figma 변형 속성 이름·값 = React props = Flutter 생성자 인자.
2. 레시피대로 Figma 세트 생성(전용 토큰 없이 조합).
3. Code Connect 매핑과 React · Flutter props 스텁.
4. Updates 항목 → Progress Board 행.

### 4.5 승격 검토

1. 제안서(`templates/promotion-proposal.md`)를 [5조건](references/minimum-set.md#승격-5조건)에 대조.
2. 승인 또는 반려 사유를 결정 기록(`templates/decision-record.md`)으로 남긴다.
3. 승인 시 4.2 절차.
4. 결과를 Updates 에 **결정** 항목으로 기록(승인·반려 모두).

### 4.6 현황 갱신

로드맵 보드의 **업무 카드** 상태가 바뀌면 Progress Board 의 대응 **진행 행**을 함께 갱신한다
(상태 · 최종 갱신일 · 링크). 상태 어휘는 두 보드가 같다(예정 · 진행중 · 완료 · 보류).

## 5. 계층 선택 요약

| 쓰는 곳 | 계층 |
|---|---|
| 한 컴포넌트만 | 컴포넌트 로컬 — 메인 컴포넌트 안에서 Semantic 바인딩(없으면 primitive 허용). **화면 인스턴스에서는 금지** |
| 한 모듈 안 둘 이상 | Module 토큰 (`commerce/` · `messenger/`) |
| Core 둘 이상 또는 모듈 둘 이상 | Semantic |
| 브랜드마다 다름 | Brand 램프 |

## 6. 검증 체크리스트

모든 쓰기 뒤 자동 실행한다(`scripts/lint.py` 가 1–7, `scripts/audit_log.py` 가 8).

1. **이름 린트** — 문법 위반, 컴포넌트명 포함, 미승인 어휘
2. **참조 린트** — Semantic · Module 의 hex 직접 값, 모듈 간 참조
3. **모드 완성도** — 모든 모드에 값 존재
4. **대비** — fg · bg 조합 레시피 기준(텍스트 4.5:1, 아이콘·테두리 3:1)
5. **scope** — `ALL_SCOPES` 없음
6. **패리티** — Figma 변수 수 = tokens.json = CSS = Dart
7. **폐기 스캔** — Deprecated 토큰 사용처
8. **기록 완료** — 이번 작업의 Updates 항목 존재, 6필드 모두 채움(비고 "없음" 허용, 빈칸 실패),
   수정자 비어 있지 않음, 영향 행의 최종 갱신일이 Updates 날짜와 같음

## 7. 자율 범위와 확인 범위

**묻지 않고 진행** — 문법에 맞는 이름 변환, scope 지정, alias 연결, 문서 프레임 갱신, 코드 생성,
검증 실행, Updates 항목 작성, Progress Board 행 갱신.

**반드시 확인** — 새 어휘 추가, 최소 세트 밖 토큰 생성, 토큰 이름 변경 · 삭제, Brand 모드 추가,
기존 라이브러리 Deprecated 처리, major 버전 올림, Updates 항목의 삭제 · 수정.

> 확인 범위의 작업은 `AskUserQuestion` 으로 묻고, 답을 받기 전에는 쓰지 않는다.

## 8. 요약

**디자이너용** — 변수는 Figma 에서만 만들고 이름은 문법표에서 고른다. 화면에서는 Semantic 만 바인딩한다.
새 토큰이 필요하면 승격 제안서를 채우고, 직접 고친 것도 Updates 에 한 줄 남기고 Progress Board 상태를 바꾼다.

**개발자용** — 토큰 패키지만 설치하고 생성 파일을 수정하지 않는다. 컴포넌트 props 는 Figma 변형 이름과 같으니
디자인 스펙을 그대로 읽는다. 값이 틀리면 코드가 아니라 Figma 변수 수정을 요청한다.
릴리스 후 Progress Board 의 React · Flutter 열을 "반영" 또는 "검증 완료"로 올린다.

## 9. 이 저장소(NDS 문서)와의 관계

이 저장소는 NDS Figma 를 읽어 옮긴 **문서 저장소**이며 `CLAUDE.md` 의 `[F]` / `[?]` / `[A]` 규칙이 그대로 적용된다.
통합 DS 작업 중 NDS 원본에서 새로 확인한 사실은 이 저장소 문서에 `[F]` + 노드 ID 로 반영하고,
통합 방향에 대한 제안은 `design-system/guidelines/ai-guidelines.md` 에만 `[A]` 로 둔다.
