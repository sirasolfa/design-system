#!/usr/bin/env python3
"""문서 안의 상대 링크와 앵커가 실제로 존재하는지 검사한다.

커밋 전에 실행하세요.  깨진 것이 없으면 종료 코드 0, 있으면 1.

    python3 scripts/check-links.py

GitHub 의 헤딩 슬러그 규칙을 그대로 구현한다:
  1. 소문자로
  2. 영숫자(유니코드) · 하이픈 · 언더스코어 · 공백을 제외한 문자 제거
  3. 공백 **1개당** 하이픈 1개  (`—` 나 ` / ` 가 지워지면 이중 하이픈이 된다)
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s", "-", text)
    return text.strip("-")


def markdown_files() -> list[str]:
    files = ["README.md"] + glob.glob("design-system/**/*.md", recursive=True)
    return [f for f in files if os.path.exists(f)]


def main() -> int:
    os.chdir(ROOT)
    files = markdown_files()

    anchors: dict[str, set[str]] = {}
    for f in files:
        found = set()
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"^#{1,6}\s+(.*)$", line)
                if m:
                    found.add(slug(m.group(1)))
        anchors[os.path.normpath(f)] = found

    broken = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            body = fh.read()
        for m in re.finditer(r"\]\(([^)]+)\)", body):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, frag = target.partition("#")
            resolved = (
                os.path.normpath(os.path.join(os.path.dirname(f), path))
                if path
                else os.path.normpath(f)
            )
            if path and not os.path.exists(resolved):
                broken.append((f, target, "파일 없음"))
                continue
            if frag and frag not in anchors.get(resolved, set()):
                broken.append((f, target, "앵커 없음"))

    if broken:
        print(f"깨진 링크 {len(broken)}건:")
        for f, target, why in broken:
            print(f"  {f}  ->  {target}   ({why})")
        return 1

    print(f"OK — {len(files)}개 파일의 상대 링크·앵커 모두 유효")
    return 0


if __name__ == "__main__":
    sys.exit(main())
