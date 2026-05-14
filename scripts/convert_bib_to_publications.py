#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

BIB_PATH = Path("tmp/papers.bib")
OUT_DIR = Path("_publications")

TYPE_MAP = {
    "inproceedings": "Conference",
    "article": "Journal",
    "phdthesis": "Thesis",
    "mastersthesis": "Thesis",
}

def strip_outer_braces(s: str) -> str:
    s = s.strip()
    while len(s) >= 2 and s[0] == "{" and s[-1] == "}":
        s = s[1:-1].strip()
    return s

def clean_value(v: str) -> str:
    v = v.strip().rstrip(",").strip()
    if len(v) >= 2 and ((v[0] == "{" and v[-1] == "}") or (v[0] == '"' and v[-1] == '"')):
        v = v[1:-1]
    v = v.replace("\\&", "&")
    v = v.replace("{", "").replace("}", "")
    return v.strip()

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80] or "publication"

def split_entries(bib: str) -> list[tuple[str, str, str]]:
    entries = []
    i = 0
    while True:
        m = re.search(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", bib[i:])
        if not m:
            break
        typ = m.group(1)
        key = m.group(2)
        start = i + m.start()
        body_start = i + m.end()
        depth = 1
        j = body_start
        while j < len(bib) and depth > 0:
            if bib[j] == "{":
                depth += 1
            elif bib[j] == "}":
                depth -= 1
            j += 1
        body = bib[body_start:j-1]
        entries.append((typ, key, body))
        i = j
    return entries

def parse_fields(body: str) -> dict[str, str]:
    fields = {}
    # field = { possibly nested-ish value }, line-oriented enough for this bib file
    pos = 0
    while pos < len(body):
        m = re.search(r"(\w+)\s*=", body[pos:])
        if not m:
            break
        name = m.group(1).lower()
        value_start = pos + m.end()
        while value_start < len(body) and body[value_start].isspace():
            value_start += 1

        if value_start < len(body) and body[value_start] in ['{', '"']:
            open_ch = body[value_start]
            close_ch = "}" if open_ch == "{" else '"'
            j = value_start + 1
            depth = 1 if open_ch == "{" else 0
            while j < len(body):
                ch = body[j]
                if open_ch == "{":
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            j += 1
                            break
                else:
                    if ch == close_ch and body[j-1] != "\\":
                        j += 1
                        break
                j += 1
            raw = body[value_start:j]
            pos = j
        else:
            j = body.find(",", value_start)
            if j == -1:
                raw = body[value_start:]
                pos = len(body)
            else:
                raw = body[value_start:j]
                pos = j + 1

        fields[name] = clean_value(raw)
    return fields

def author_list(author_field: str) -> list[str]:
    if not author_field:
        return []
    authors = [a.strip() for a in re.split(r"\s+and\s+", author_field)]
    out = []
    for a in authors:
        if "," in a:
            last, first = [x.strip() for x in a.split(",", 1)]
            out.append(f"{first} {last}".strip())
        else:
            out.append(a)
    return out

def yaml_quote(s: str) -> str:
    s = s.replace('"', '\\"')
    return f'"{s}"'

def main() -> None:
    if not BIB_PATH.exists():
        raise SystemExit(f"Missing {BIB_PATH}. Run: git show backup/al-folio-current:_bibliography/papers.bib > tmp/papers.bib")

    bib = BIB_PATH.read_text(encoding="utf-8")

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    entries = split_entries(bib)
    count = 0

    for typ, key, body in entries:
        if key.lower() in {"aps"}:
            continue

        f = parse_fields(body)
        title = f.get("title", key)
        year = f.get("year", "9999")
        selected = f.get("selected", "false").lower() == "true"

        venue = (
            f.get("booktitle")
            or f.get("journal")
            or f.get("school")
            or TYPE_MAP.get(typ.lower(), typ)
        )

        authors = author_list(f.get("author", ""))

        year_dir = OUT_DIR / year
        year_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{year}-{slugify(key)}.md"
        out_path = year_dir / filename

        # Keep date monotonic within year, but approximate.
        date = f"{year}-06-01 12:00:00 +0000"

        lines = [
            "---",
            f"title: {yaml_quote(title)}",
            f"date: {date}",
            f"selected: {'true' if selected else 'false'}",
            f"pub: {yaml_quote(venue)}",
            f"pub_date: {yaml_quote(year)}",
        ]

        if f.get("abstract"):
            lines += ["abstract: >-", f"  {f['abstract']}"]

        lines += ["authors:"]
        for a in authors:
            lines.append(f"  - {a}")

        links = {}
        if f.get("html"):
            links["Paper"] = f["html"]
        if f.get("pdf"):
            pdf = f["pdf"]
            if not pdf.startswith("http"):
                pdf = f"/assets/pdf/{pdf}"
            links["PDF"] = pdf
        if f.get("code"):
            links["Code"] = f["code"]
        if f.get("website"):
            links["Website"] = f["website"]

        if links:
            lines.append("links:")
            for name, url in links.items():
                lines.append(f"  {name}: {url}")

        if f.get("note"):
            lines.append(f"pub_last: {yaml_quote(f['note'])}")

        lines.append("---")
        lines.append("")

        out_path.write_text("\n".join(lines), encoding="utf-8")
        count += 1

    print(f"Generated {count} publication files under {OUT_DIR}")

if __name__ == "__main__":
    main()
