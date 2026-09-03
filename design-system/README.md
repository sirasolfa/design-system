# design-system/

NDS(NOVERA Design System) 문서 세트. 진입점은 저장소 루트의 [`README.md`](../README.md)입니다.

## 인덱스

### foundations — 토큰 `[F]`
| 문서 | 내용 | Figma 노드 |
|---|---|---|
| [color.md](foundations/color.md) | primitive 팔레트 · semantic 토큰 | `1:160`, `144:419` |
| [typography.md](foundations/typography.md) | 폰트 · 웨이트 · 텍스트 스타일 | `139:1666`, `163:998` |
| [layout.md](foundations/layout.md) | gap · spacing · grid · breakpoint | `170:1666`, `380:1802` |
| [shape.md](foundations/shape.md) | rounded · border-width | `170:1660` |
| [elevation.md](foundations/elevation.md) | shadow | `749:4126` |
| [iconography.md](foundations/iconography.md) | 아이콘 그리드 · 사이즈 · 목록 | `2442:11467`, `1209:12283` |
| [brand.md](foundations/brand.md) | 로고 · 파비콘 · OG | `1621:20549`, `2079:2181` |

### components — 인벤토리와 베리언트 `[F]`
| 문서 | Figma 노드 |
|---|---|
| [README.md](components/README.md) — 전체 인벤토리·상태 | Overview `1183:7436` |
| [content-display.md](components/content-display.md) | 페이지 `1595:11126` |
| [overlay.md](components/overlay.md) | 페이지 `1595:11129` |
| [inputs.md](components/inputs.md) | Overview `1192:7929` |
| [button.md](components/button.md) | Overview `1192:6212` |
| [navigation.md](components/navigation.md) | Overview `1183:7464` |
| [indicator-status.md](components/indicator-status.md) | Overview `1192:7796` |

### patterns — 조합 패턴 `[F]`
| 문서 | 내용 |
|---|---|
| [README.md](patterns/README.md) | `(Usage)` 가이드 10종의 절 구성과 공통 템플릿 |
| [commerce.md](patterns/commerce.md) | 상품 카드 · 장바구니 · 이벤트 카드 · 검색 |

### guidelines
| 문서 | 성격 |
|---|---|
| [naming.md](guidelines/naming.md) | `[F]` 네이밍 규칙 (Change Log 원문) |
| [changelog.md](guidelines/changelog.md) | `[F]` Change Log 전문 |
| [ai-guidelines.md](guidelines/ai-guidelines.md) | **`[A]` AI 제안 — 이 파일만 제안입니다** |

---

## 표기 규약

| 표기 | 뜻 |
|---|---|
| `[F]` | Figma에서 직접 읽은 사실. 노드 ID를 병기합니다. |
| `[?]` | Figma에 존재하지만 값이 미확인이거나, 시안 내부에서 값이 어긋나는 항목. |
| `[A]` | AI 제안. `guidelines/ai-guidelines.md`에만 존재합니다. |

토큰 이름은 **Figma에 적힌 표기 그대로** 씁니다.

- 변수(variable) 경로는 슬래시: `color/blue/600`, `layout/gap/16`
- 문서 표(Semantic Color Token 페이지 등)에 인쇄된 표기는 점: `color.text.secondary`

두 표기는 같은 대상을 가리키지만 **완전히 1:1은 아닙니다**(예: 표의 `color.bg.default` ↔ 변수 `color/bg/surface/default`).
이 문서는 둘을 나란히 적고, 다른 부분은 그때마다 표시합니다.

---

## 원본 갱신 방법

Figma MCP가 붙어 있는 세션에서 아래 순서로 다시 읽으면 됩니다.

```
# 1. 페이지 목록
get_metadata(fileKey="OJqTwQ8gHDGcvOOkOfYRgM")              # nodeId 없이 호출

# 2. 페이지 구조 (출력이 크면 파일로 저장됨)
get_metadata(fileKey=..., nodeId="0:1")                      # Foundation
get_metadata(fileKey=..., nodeId="1595:11126")               # Content Display
get_metadata(fileKey=..., nodeId="1595:11129")               # Overlay

# 3. 토큰 값 — 해당 프레임이 "사용 중인" 변수만 반환된다
get_variable_defs(fileKey=..., nodeId="113:2114")            # primitive 팔레트
get_variable_defs(fileKey=..., nodeId="163:998")             # 텍스트 스타일 대부분
get_variable_defs(fileKey=..., nodeId="749:4126")            # shadow

# 4. 표/문구는 스크린샷으로 읽는 편이 저렴하다
get_screenshot(fileKey=..., nodeId="196:5392", enableBase64Response=true)
```

### 조사하며 걸린 제약

- `get_variable_defs`는 **그 노드가 실제로 쓰는 변수만** 반환합니다. 컬렉션 전체 덤프가 아닙니다.
  팔레트에서 값이 안 나오는 칸(예: 조사 시점의 `color/blue/500`)은 스크린샷으로 확인했습니다.
- **레이어 이름이 곧 텍스트 내용**인 경우가 많아, `get_metadata` XML의 `name=` 만 훑어도
  표 본문을 상당 부분 복원할 수 있습니다. 이 문서의 "역할 설명" 문구 다수가 그 경로로 옮겨온 것입니다.
- **단, 컴포넌트의 `(Usage)` 가이드는 예외입니다.** 레이어 이름이 `Guide` · `Section Title` ·
  `Description` 같은 껍데기라 `get_metadata` 로는 내용을 읽을 수 없습니다.
  `get_screenshot`(작은 프레임) 또는 `get_design_context`(텍스트만 필요할 때,
  `excludeScreenshot=true`)를 써야 합니다.
- `get_design_context` 응답 끝에는 **Component descriptions** 가 함께 옵니다 — Figma 컴포넌트에
  달아 둔 용도 설명입니다. 다른 도구로는 나오지 않습니다.
- **노드 ID는 고정이 아닙니다.** 이 문서를 처음 만든 뒤 몇 시간 만에 `Action Area(Usage)` 의
  노드 ID가 바뀌었습니다. 문서의 ID는 조회 시점의 스냅샷으로 다루세요.
- 이 실행 환경에서는 `figma.com` 직접 다운로드가 조직 egress 정책으로 **403** 입니다.
  스크린샷은 `enableBase64Response=true` 로 받아야 합니다(`curl`로는 못 받음).
- Figma **layout grid(컬럼/거터)** 는 MCP로 노출되지 않습니다. Grid 페이지에서 확정할 수 있는 건
  뷰포트 크기와 전환 기준뿐입니다.
