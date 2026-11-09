#!/usr/bin/env bash
# 스크립트 자체 검사 — 가짜 변수로 추출 이후 파이프라인 전체를 돌린다.
#   bash .claude/skills/unified-ds/scripts/selftest.sh [작업폴더]
# Style Dictionary 단계는 node_modules/style-dictionary 가 작업폴더에 있을 때만 실행한다.
set -euo pipefail
S="$(cd "$(dirname "$0")" && pwd)"
W="${1:-$(mktemp -d)}"; mkdir -p "$W"; cd "$W"
python3 "$S/fixtures/make_fixture.py" .
python3 "$S/to_dtcg.py" raw.json -o tokens.json --version 0.0.0-selftest
python3 "$S/resolve_tokens.py" tokens.json -o resolved
python3 "$S/gen_dart.py" resolved -o out/tokens.g.dart
ARGS=(--tokens tokens.json --dart out/tokens.g.dart)
if [ -d node_modules/style-dictionary ]; then
  cp "$S/style-dictionary.config.mjs" ./sd.mjs && node sd.mjs resolved out/react
  ARGS+=(--css out/react/tokens.css)
fi
python3 "$S/lint.py" "${ARGS[@]}"
