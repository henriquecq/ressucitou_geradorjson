"""Rebuild complete transcriptions explicitly verified in the third review range."""
import html
import copy
import json
from pathlib import Path
from build_reviewed_sheets import render as render_reviewed

ROOT = Path(__file__).resolve().parents[1]


def render(sheet, extended):
    if extended and sheet.get('expansions'):
        original = sheet
        sheet = copy.deepcopy(sheet)
        expanded = []
        def expand(index):
            row = original['rows'][index]
            target = original['expansions'].get(str(index))
            if not target:
                return [copy.deepcopy(row)]
            rows = copy.deepcopy(original['rows'][target[0]:target[1]])
            rows[0]['role'] = row.get('role', '')
            # Explicit entry notes in the printed abbreviated call take precedence.
            rows[0]['notes'] = copy.deepcopy(row['notes'])
            return rows
        for index in range(len(original['rows'])):
            expanded.extend(expand(index))
            block = next(((a, b) for a, b in original.get('repeatBlocks', []) if b == index + 1), None)
            if block:
                repeated = []
                for repeat_index in range(block[0], block[1]):
                    repeated.extend(expand(repeat_index))
                repeated[0]['role'] = 'A.'
                expanded.extend(repeated)
        sheet['rows'] = expanded
        sheet['repeatBlocks'] = []
    result = render_reviewed(sheet, extended).decode('utf8')
    for marker in sheet.get('redMarkers', []):
        result = result.replace(html.escape(marker), html.escape(marker[:-1]) + '<span style="color:#FF0000">*</span>')
    return result.replace('<span class="inv">@capot@ </span>',
                          '<span class="inv">@capot@ </span>' + html.escape(sheet.get('capo', ''))).encode('utf8')


def main():
    sheets = json.loads((ROOT / 'data/edicao_2026/fichas-revisao-maxima-faixa3.json').read_text(encoding='utf8'))
    for sheet in sheets:
        for extended, folder in [(False, 'html'), (True, 'html/ext')]:
            (ROOT / folder / (sheet['html'] + '.HTML')).write_bytes(render(sheet, extended))


if __name__ == '__main__':
    main()
