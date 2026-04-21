"""Scan .docx under repo for 2,5%/2.5% (excluding 22,5% IR). UTF-8 stdout."""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

PAT_25 = re.compile(r"(?<!\d)2[,.]5\s*%")
PAT_35 = re.compile(r"(?<!\d)3[,.]5\s*%")

REPO = Path(__file__).resolve().parents[1]


def docx_plain_text(path: Path) -> str:
    with zipfile.ZipFile(path, "r") as z:
        raw = z.read("word/document.xml").decode("utf-8", errors="replace")
    chunks = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", raw)
    return "".join(chunks)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    docxs = sorted(p for p in REPO.rglob("*.docx") if not p.name.startswith("~"))
    hits_25: list[tuple[str, list[str]]] = []
    summary_35: list[str] = []

    for p in docxs:
        try:
            plain = docx_plain_text(p)
        except (zipfile.BadZipFile, KeyError, OSError) as e:
            print(f"SKIP {p.relative_to(REPO)}: {e}", file=sys.stderr)
            continue
        ctxs = []
        for m in PAT_25.finditer(plain):
            start = max(0, m.start() - 60)
            ctxs.append(plain[start : m.end() + 70].replace("\n", " ")[:200])
        if ctxs:
            hits_25.append((str(p.relative_to(REPO)), ctxs))
        if PAT_35.search(plain):
            summary_35.append(str(p.relative_to(REPO)))

    print("=== DOCX com 2,5% / 2.5% (regex exclui 22,5% por lookbehind) ===\n")
    for rel, ctxs in hits_25:
        print(f"== {rel}")
        for c in ctxs[:10]:
            print(f"  {c}")
        print()

    print("\n=== DOCX que também mencionam 3,5% / 3.5% ===\n")
    for rel in summary_35:
        print(f"  {rel}")


if __name__ == "__main__":
    main()
