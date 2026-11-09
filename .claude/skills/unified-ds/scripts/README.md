# scripts — unified-ds

| 파일 | 단계 | 하는 일 |
|---|---|---|
| `figma/extract-variables.js` | 읽기 | `use_figma` 로 로컬 변수 전체 → 원시 JSON |
| `figma/read-boards.js` | 읽기 | Updates · Progress Board · Roadmap → JSON (`PAGE` 바꿔 3회 병렬) |
| `figma/write-update.js` | 기록 | "업데이트 항목" 인스턴스 1건 추가 (사전 검증 포함) |
| `figma/write-progress.js` | 기록 | "진행 행" 갱신/생성 |
| `to_dtcg.py` | 추출 | 원시 JSON → `tokens.json` (W3C DTCG, 모드는 `$extensions`) |
| `resolve_tokens.py` | 생성 | `tokens.json` → 브랜드 × 테마 해석본 4개 |
| `style-dictionary.config.mjs` | 생성 | 해석본 → `tokens.css` · `tokens.ts` (Style Dictionary v4) |
| `gen_dart.py` | 생성 | 해석본 → `tokens.g.dart` (ThemeExtension) |
| `lint.py` | 검증 | 체크리스트 1–7 (이름 · 참조 · 모드 · 대비 · scope · 패리티 · 폐기/리터럴) |
| `audit_log.py` | 검증 | 체크리스트 8 (기록 완료) + 감사의 기록 누락 |
| `changelog.py` | 기록 | Updates → `CHANGELOG.md` |
| `naming.py` | 공용 | 이름 문법 · 플랫폼 변환 (유일한 구현) |
| `tokens_lib.py` | 공용 | alias 해석 · 대비 계산 |
| `minimum_set.json` · `contrast_pairs.json` | 데이터 | references 표의 기계 판독본 |
| `selftest.sh` · `fixtures/` | 자체 검사 | 가짜 변수로 전체 파이프라인 실행 |

## 전체 흐름 (코드 내보내기)

```bash
# 1. use_figma 로 figma/extract-variables.js 실행 → 반환값을 build/raw-variables.json 에 저장
python3 scripts/to_dtcg.py build/raw-variables.json -o tokens.json --version 1.3.0
python3 scripts/resolve_tokens.py tokens.json -o build/resolved
node scripts/style-dictionary.config.mjs build/resolved dist/react
python3 scripts/gen_dart.py build/resolved -o dist/flutter/lib/tokens.g.dart
python3 scripts/lint.py --tokens tokens.json --css dist/react/tokens.css \
    --dart dist/flutter/lib/tokens.g.dart --figma-count <Figma 공개 변수 수> --src src lib
# 2. use_figma 로 figma/write-update.js (릴리스) → figma/write-progress.js (React · Flutter 열)
# 3. use_figma 로 figma/read-boards.js (Updates) → updates.json
python3 scripts/changelog.py updates.json -o CHANGELOG.md
python3 scripts/audit_log.py --updates updates.json --progress progress.json \
    --expect-title "릴리스 · …" --expect-date YYYY.MM.DD --expect-rows "…"
```

`style-dictionary.config.mjs` 는 `style-dictionary@4` 가 설치된 토큰 패키지 저장소 안에서 실행한다
(ESM import 는 파일 위치 기준으로 해석되므로, 필요하면 패키지 저장소로 복사해 쓴다).
