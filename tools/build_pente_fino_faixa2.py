"""Reproduce the complete 2026 sheet confirmed by the second detailed review."""
import json
from pathlib import Path
from build_complementary_sheets import render as render_complementary

ROOT = Path(__file__).resolve().parents[1]


def render(sheet, extended):
    content = render_complementary(sheet, extended)
    if sheet['html'] == 'NOLI ME TANGERE':
        content = content.replace(b'(melisma)', b'<FONT COLOR="#FF0000">(melisma)')
    return content


def main():
    sheets = json.loads((ROOT/'data/edicao_2026/fichas-pente-fino-2-faixa2.json').read_text(encoding='utf8'))
    for sheet in sheets:
        for extended, folder in [(False,'html'),(True,'html/ext')]:
            content = render(sheet,extended)
            (ROOT/folder/(sheet['html']+'.HTML')).write_bytes(content)


if __name__ == '__main__':
    main()
