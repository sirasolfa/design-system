# 컬러칩 문서 프레임

토큰 생성 · 변경 뒤 해당 페이지의 문서 프레임을 갱신한다(묻지 않고 진행하는 범위).

| 컬렉션 | 페이지 |
|---|---|
| Primitive | `Color — Primitive` |
| Semantic (+ Module) | `Color — Semantic (Light · Dark)` |
| Brand | `Brand Modes (NOVERA · 1CHON)` |

## 구조

```
Frame "{property} — {컬렉션}"            (VERTICAL auto-layout)
├── Title       TEXT  "bg · Semantic"
├── Header row  (HORIZONTAL)  토큰 | Light | Dark | alias(Light) | alias(Dark) | scope
└── Chip row × N  (HORIZONTAL)  — 한 행 = 한 변수
    ├── name    TEXT  "bg/neutral-solid"
    ├── chip    RECT 40×40, fill = 변수 바인딩 · 프레임에 setExplicitVariableModeForCollection(Light)
    ├── chip    RECT 40×40, fill = 변수 바인딩 · 프레임에 setExplicitVariableModeForCollection(Dark)
    ├── alias   TEXT  "{brand.primary.600}"
    ├── alias   TEXT  "{color.gray.50}"
    └── scope   TEXT  "FRAME_FILL · SHAPE_FILL"
```

Brand 페이지는 열이 `NOVERA | 1CHON` 이다. Primitive 페이지는 램프별 가로 줄(50 → 950).

## 규칙

- 칩 색은 hex 를 칠하지 않고 **변수에 바인딩**한다(`setBoundVariableForPaint`). 값이 바뀌면 칩이 따라온다.
- 모드 열은 칩을 감싼 셀 프레임에 `setExplicitVariableModeForCollection` 으로 고정한다.
- 행 순서는 [minimum-set.md](../references/minimum-set.md) 표 순서, 세트 밖 토큰은 뒤에 이름순.
- 갱신은 **변경된 행만** 다시 그린다. 행 식별은 name TEXT 내용.
- Deprecated 토큰 행은 name 에 취소선 + `→ 대체 토큰` 텍스트.
- 반투명 bg(`bg/overlay` · `bg/state-*`)는 체커보드 위에 칩을 둔다.
