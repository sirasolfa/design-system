#!/usr/bin/env python3
"""Updates 페이지(read-boards.js 'Updates') → 코드 저장소 CHANGELOG.md.

    python3 changelog.py updates.json -o CHANGELOG.md

- 원본은 Updates 페이지다. CHANGELOG.md 는 생성물이며 손으로 고치지 않는다.
- "릴리스" 항목의 비고에서 `v1.2.3` 을 찾아 버전 머리글을 만든다. 그보다 새 항목은 Unreleased.
- 둘이 다르면 Updates 가 맞다 — 다시 생성한다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("updates")
    ap.add_argument("-o", "--out", default="CHANGELOG.md")
    a = ap.parse_args()

    entries = json.load(open(a.updates, encoding="utf-8"))["entries"]
    entries.sort(key=lambda e: (e["날짜"], -e.get("order", 0)), reverse=True)

    out = ["# Changelog", "",
           "> 생성 파일 — 수정 금지. 원본은 Figma 통합 DS 파일의 **Updates · Changelog** 페이지입니다.", ""]
    section = "## Unreleased"
    out += [section, ""]
    empty = True
    for e in entries:
        if e.get("유형") == "릴리스":
            m = re.search(r"v?(\d+\.\d+\.\d+)", e.get("비고", "") + " " + e.get("타이틀", ""))
            ver = m.group(1) if m else "?"
            if empty and section == "## Unreleased":
                out += ["_없음_", ""]
            section = f"## {ver} — {e['날짜']}"
            out += [section, "", e.get("상세", ""), ""]
            empty = True
            continue
        summary = e["타이틀"].split(" · ", 1)[-1]
        out.append(f"- **{e.get('유형')}** {summary} — {e.get('범위', '')} ({e['날짜']})")
        for line in e.get("상세", "").splitlines():
            if line.strip():
                out.append(f"  - {line.strip()}")
        if e.get("비고") and e["비고"] != "없음":
            out.append(f"  - 비고: {e['비고']}")
        out.append(f"  - 수정자: {e.get('수정자', '')}")
        empty = False
    if empty:
        out += ["_없음_"]
    open(a.out, "w", encoding="utf-8").write("\n".join(out).rstrip() + "\n")
    print(f"{a.out}: {len(entries)}건")
    return 0


if __name__ == "__main__":
    sys.exit(main())
