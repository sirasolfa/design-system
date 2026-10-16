# CLAUDE.md — 이 저장소에서 일하는 방법

NDS(NOVERA Design System) **문서 저장소**입니다. 코드는 없고 마크다운만 있습니다.
원본은 Figma이고, 이 저장소는 그것을 읽어 옮긴 결과물입니다.

## 가장 중요한 규칙 — 사실과 제안을 섞지 않는다

| 표기 | 뜻 | 둘 곳 |
|---|---|---|
| `[F]` | Figma에서 **직접 읽은 값**. 노드 ID를 반드시 병기 | `foundations/` · `components/` · `patterns/` · `guidelines/naming.md` · `guidelines/changelog.md` |
| `[?]` | 값을 못 읽었거나 **시안 내부에서 어긋나는** 항목 | 각 문서의 "확인 필요" 절 |
| `[A]` | Figma에 근거 없는 **AI 제안** | **`guidelines/ai-guidelines.md` 한 파일에만** |

- 사실 문서 본문에 `[A]` 를 섞지 않는다. 링크만 건다.
- **추정값을 적지 않는다.** 못 읽었으면 `[?]` 로 비워 둔다.
  (예: Grid 컬럼/거터는 Figma layout grid 속성이라 MCP로 안 나온다 → 추정 금지)
- `[A]` 항목에는 "근거"와 "확정 조건"을 함께 적는다.

## Figma 원본

| | |
|---|---|
| File key | `OJqTwQ8gHDGcvOOkOfYRgM` |
| 페이지 | Overview `1183:7436` · Foundation `0:1` · • Content Display `1595:11126` · • Overlay `1595:11129` |
| 적용 서비스 | [`sirasolfa/shop-lab`](https://github.com/sirasolfa/shop-lab) |

## Figma 읽는 법 — 이 파일에서 실제로 통한 방법

순서대로 시도하면 토큰을 가장 적게 씁니다.

1. **`use_figma` 읽기 전용 스크립트가 가장 싸다.** 원하는 것만 골라 `return` 하면 됩니다.
   ```js
   const p = figma.root.children.find(x => x.name.includes('Overlay'));
   await figma.setCurrentPageAsync(p);          // 동기 설정은 동작하지 않음
   const g = await figma.getNodeByIdAsync('4493:25180');
   return g.query('TEXT').toArray()
     .filter(t => typeof t.fontSize === 'number' && t.fontSize >= 16)
     .map(t => ({ fs: t.fontSize, op: Math.round(t.opacity * 100), chars: t.characters.slice(0, 220) }));
   ```
   호출 전 **반드시 `figma-use` 스킬을 로드**하고 `skillNames` 에 넣습니다.
2. **`get_metadata`** — 레이어 이름만 필요할 때. 출력이 크면 파일로 떨어지니 python으로 파싱.
3. **`get_design_context`** (`excludeScreenshot: true`) — 작은 Title Container의 정확한 문구,
   그리고 응답 끝의 **Component descriptions**(Figma 컴포넌트 설명)를 얻을 때. 다른 도구로는 안 나옵니다.
4. **`get_screenshot`** — 표·다이어그램·Do/Don't처럼 레이아웃이 의미를 갖는 것. 이 환경에서는
   `figma.com` 직접 다운로드가 egress 정책으로 403이라 **`enableBase64Response: true`** 가 필수입니다.

### 함정

- **가이드 설명 문장은 레이어 이름에 없다.** `get_metadata` 로는 `Guide` · `Section Title` ·
  `Description` 같은 껍데기만 보입니다. 예외로 `Accordion(Usage)` 는 설명이 레이어 이름에
  그대로 들어 있어 자동 추출이 됩니다.
- **투명도 50%(`opacity-50`)는 TBD 초안**입니다. 확정 규칙과 구분해 적습니다.
  `use_figma` 로 `t.opacity` 를 함께 뽑으면 바로 식별됩니다.
- **프레임 이름을 믿지 말 것.** `Search(Usage)` 가 실제로는 Bottom Sheet 가이드였습니다
  (2026-10-15 개명 완료). 가이드 식별은 **Title Container 의 Guide/Subtitle 텍스트**로 합니다.
- **베리언트 목록만 보면 프로퍼티의 절반도 모른다.** boolean / 텍스트 / Instance Swap / Slot
  프로퍼티는 Usage 가이드에만 나옵니다. Accordion 은 베리언트 3개 뒤에 8개가 더 있습니다.
- **노드 ID와 프레임 이름이 자주 바뀐다.** 2026-09-02 → 10-16 사이에 가이드 4종 신설,
  `Action Area(Usage)` → `Sheet(Usage)` 개명, Toast 전면 재작성이 있었습니다.
  문서의 ID는 조회 시점 스냅샷으로 다루고, 작업 전 현재 상태를 다시 확인합니다.

## 문서 작성 규칙

- 토큰 이름은 **Figma 표기 그대로**. 변수는 슬래시(`color/blue/600`), 문서 표는 점(`color.text.secondary`).
  둘이 구조까지 다른 경우가 있으므로(`color.bg.default` ↔ `color/bg/surface/default`) 나란히 적습니다.
- **오타도 원문 그대로 옮기고 ※오타 표시**를 답니다. 임의로 고치지 않습니다
  (`priamry`, `defualt`, `discout`, `hypen`, `sementic` 등).
- 시안 문구를 옮길 때는 인용문(`>`)을 쓰고 "시안 원문"임을 밝힙니다.

### 링크·앵커 검사 (커밋 전 필수)

```bash
python3 scripts/check-links.py
```

GitHub 앵커 슬러그는 **구두점 제거 후 공백 1개당 하이픈 1개**입니다.
`Search(Usage)` → `searchusage`(괄호가 사라져 하이픈 없음), `— ` 나 ` / ` 가 들어가면 `--`(이중 하이픈).
손으로 쓰지 말고 스크립트로 확인하세요.

## 커밋

- 메시지는 한국어, 본문에 **무엇을 왜 바꿨는지**와 새로 확인된 사실을 적습니다.
- 디자인에 요청할 것이 생기면 `guidelines/design-requests.md` 에 노드 ID와 함께 추가합니다.

## 문서 지도

```
README.md                      진입점
design-system/
├── foundations/   color · typography · layout · shape · elevation · iconography · brand
├── components/    README(인벤토리 50종) + 카테고리 6종
├── patterns/      README((Usage) 가이드 목록) · commerce
└── guidelines/    design-requests · naming · changelog · ai-guidelines
```
