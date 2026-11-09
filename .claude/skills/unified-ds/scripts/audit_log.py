#!/usr/bin/env python3
"""기록 검사 — SKILL.md 체크리스트 8(기록 완료)과 감사의 "기록 누락" 리포트.

    # 쓰기 작업 직후: 이번 항목이 제대로 남았는지
    python3 audit_log.py --updates updates.json --progress progress.json \
        --expect-title "추가 · Semantic 최소 세트 42개" --expect-date 2026.11.09 \
        --expect-rows "Semantic 컬러"

    # 감사: 변수 diff 중 Updates 에 언급이 없는 것
    python3 audit_log.py --updates updates.json --progress progress.json \
        --diff tokens.prev.json tokens.json

입력 updates.json · progress.json 은 scripts/figma/read-boards.js 반환값을 저장한 것.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

FIELDS = ["날짜", "타이틀", "상세", "범위", "비고", "수정자"]
TYPES = ["추가", "변경", "이름변경", "폐기", "삭제", "문서", "릴리스", "결정"]


def names(path: str) -> dict[str, dict]:
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from tokens_lib import NS, index, load
    return {n: t["$extensions"][NS]["modes"] for n, t in index(load(path)).items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--updates", required=True)
    ap.add_argument("--progress")
    ap.add_argument("--expect-title")
    ap.add_argument("--expect-date")
    ap.add_argument("--expect-rows", nargs="*", default=[])
    ap.add_argument("--diff", nargs=2, metavar=("PREV", "CURR"))
    a = ap.parse_args()

    ups = json.load(open(a.updates, encoding="utf-8"))["entries"]
    rows = json.load(open(a.progress, encoding="utf-8"))["rows"] if a.progress else []
    fails, missing = [], []

    # 항목 형식
    for e in ups:
        where = f"[{e.get('month')}#{e.get('order')}] {e.get('타이틀', '')!r}"
        for f in FIELDS:
            if not str(e.get(f, "")).strip():
                fails.append(f"{where}: {f} 빈칸")
        if e.get("수정자", "").strip() in ("", "이름 (역할)"):
            missing.append(f"{where}: 수정자 비어 있음/기본값")
        if e.get("유형") not in TYPES:
            fails.append(f"{where}: 유형 뱃지 '{e.get('유형')}'")
        elif not e.get("타이틀", "").startswith(e["유형"] + " · "):
            fails.append(f"{where}: 타이틀이 '{e['유형']} · ' 로 시작하지 않음")
        if not re.fullmatch(r"\d{4}\.\d{2}\.\d{2}", e.get("날짜", "")):
            fails.append(f"{where}: 날짜 형식")
        elif e.get("month") and not e["날짜"].startswith(e["month"]):
            fails.append(f"{where}: 날짜가 월 섹션 {e['month']} 과 다름")

    # 정렬: 월 내림차순, 월 안에서 날짜 내림차순
    for i in range(1, len(ups)):
        p, c = ups[i - 1], ups[i]
        if p.get("month") == c.get("month") and p.get("날짜", "") < c.get("날짜", ""):
            fails.append(f"정렬: {c['타이틀']!r} 가 더 최근인데 아래에 있음")

    # 행 ↔ Updates 일치
    titles = {e.get("타이틀"): e for e in ups}
    for r in rows:
        link = r.get("링크")
        if link and link not in titles and link != "최근 Updates 항목":
            missing.append(f"행 {r.get('항목')!r}: 링크 {link!r} 에 해당하는 Updates 항목 없음")
        elif link in titles and titles[link]["날짜"] != r.get("최종 갱신일"):
            fails.append(f"행 {r.get('항목')!r}: 최종 갱신일 {r.get('최종 갱신일')} ≠ Updates {titles[link]['날짜']}")

    # 이번 작업 기록 완료
    if a.expect_title:
        e = titles.get(a.expect_title)
        if not e:
            fails.append(f"기록 완료: Updates 에 {a.expect_title!r} 없음")
        elif a.expect_date and e["날짜"] != a.expect_date:
            fails.append(f"기록 완료: 날짜 {e['날짜']} ≠ {a.expect_date}")
        for item in a.expect_rows:
            r = next((r for r in rows if r.get("항목") == item), None)
            if not r:
                fails.append(f"기록 완료: Progress Board 행 {item!r} 없음")
            else:
                if r.get("링크") != a.expect_title:
                    fails.append(f"기록 완료: 행 {item!r} 링크 {r.get('링크')!r}")
                if a.expect_date and r.get("최종 갱신일") != a.expect_date:
                    fails.append(f"기록 완료: 행 {item!r} 최종 갱신일 {r.get('최종 갱신일')}")

    # 감사: 변수 diff 중 기록 누락
    if a.diff:
        prev, curr = names(a.diff[0]), names(a.diff[1])
        changed = sorted(set(prev) ^ set(curr)) + sorted(n for n in set(prev) & set(curr) if prev[n] != curr[n])
        corpus = "\n".join(f"{e.get('상세', '')} {e.get('범위', '')} {e.get('타이틀', '')}" for e in ups)
        for n in changed:
            if n not in corpus:
                missing.append(f"변수 diff {n}: Updates 에 언급 없음")

    print(f"Updates {len(ups)}건 · Progress 행 {len(rows)}개")
    for f in fails:
        print("  FAIL ", f)
    for m in missing:
        print("  기록 누락 ", m)
    print("결과:", "실패" if fails or (a.expect_title and missing) else "통과")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
