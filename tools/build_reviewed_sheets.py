"""Build only the explicitly reviewed 2026 transcriptions, preserving the WebView HTML contract."""
import copy
import html
import json
import re
from pathlib import Path
from chord_diagrams import diagrams_markup

ROOT = Path(__file__).resolve().parents[1]


def line_markup(row):
    if row.get('heading'):
        return ['', '<FONT COLOR="#000000"><b>' + html.escape(row['text']) + '</b>', '']
    text = html.escape(row['text'], quote=False)
    if row.get('bold'):
        text = '<b>' + text + '</b>'
    role = row.get('role', '')
    prefix = role.ljust(4) if role else (' ' * 4 if row.get('bold') else ' ' * 4)
    notes = ''
    for col, note in sorted(row.get('notes', [])):
        target = col + 4
        # Several cadential chords can fall on the same syllable. Keep their
        # order and a separating space in the monospaced representation.
        if target < len(notes) + 1 and notes:
            target = len(notes) + 1
        notes += ' ' * (target - len(notes)) + note
    result = []
    if notes:
        result.append('<FONT COLOR="#FF0000">' + notes)
    result.append('<FONT COLOR="#000000">' + prefix + text)
    return result


def render(sheet, extended):
    rows = copy.deepcopy(sheet['rows'])
    if extended:
        for start, end in reversed(sheet.get('repeatBlocks', [])):
            repeated = copy.deepcopy(rows[start:end])
            repeated[0]['role'] = 'A.'
            rows[end:end] = repeated
        if sheet.get('expandRefrain'):
            start = sheet.get('refrainStart', 0)
            refrain = copy.deepcopy(sheet['rows'][start:start + sheet['refrainLength']])
            expanded = []
            for row in rows:
                if row.get('abbreviatedRefrain'):
                    block = copy.deepcopy(refrain)
                    block[0]['role'] = 'A.'
                    expanded.extend(block)
                else:
                    expanded.append(row)
            rows = expanded
    header = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><style>body{margin:0px;-webkit-user-select: none;} .inv{display:none} h1{margin:0px;} .html_canto{font-size:12px;padding-left:5px;white-space:pre;font-family:monospace;} </style></head>'
    result = [header, f'<body class="html_canto" style="background-color: {sheet["color"]};"><div>',
              '<FONT COLOR="#FF0000"><H1><b>' + html.escape(sheet['title']) + '</b></H1>',
              '<FONT COLOR="#000000"><b>' + html.escape(sheet['subtitle']) + '</b>', '',
              '<span class="inv">@capot@ </span>', '<span class="inv">@transp@</span>', '']
    if sheet.get('intro'):
        result += ['<FONT COLOR="#000000">    ' + html.escape(sheet['intro']), '']
    for index, row in enumerate(rows):
        if row.get('role') or row.get('blankBefore'):
            result.append('')
        if index == len(rows) - 1 and sheet.get('rubric'):
            result += ['', '<FONT COLOR="#FF0000">    ' + html.escape(sheet['rubric']), '']
        if row.get('annotation'):
            result.append('<FONT COLOR="#000000">    <i>' + html.escape(row['annotation']) + '</i>')
        markup = line_markup(row)
        repeat = next(((start, end) for start, end in sheet.get('repeatBlocks', [])
                       if start <= index < end), None) if not extended else None
        if repeat:
            start, end = repeat
            width = max(4 + len(sheet['rows'][i]['text']) for i in range(start, end)) + 4
            width = max(width, max(len(line_markup(sheet['rows'][i])[0].split('>', 1)[-1])
                                   for i in range(start, end)))
            for position, line in enumerate(markup):
                # Close FONT before the bar so the bracket and label stay black.
                visible = html.unescape(re.sub('<[^>]*>', '', line))
                line += ' ' * max(1, width - len(visible)) + '</font><font color="#000000">|</font>'
                if index == start + (end - start) // 2 and position == 0:
                    label = sheet.get('repeatLabels', {}).get(str(end), 'BIS A.')
                    line += '<font color="#000000"> ' + html.escape(label) + '</font>'
                markup[position] = line
        result.extend(markup)
    if sheet.get('footnote'):
        result += ['', '<FONT COLOR="#000000">    ' + html.escape(sheet['footnote'])]
    if sheet.get('diagrams'):
        result += ['', '<FONT COLOR="#000000">' + diagrams_markup(sheet['diagrams'])]
    result += ['', '</div></body></html>', '']
    text = '\n'.join(result).replace('\r\n', '\n').replace('\r', '\n')
    return text.replace('\n', '\r\n').encode('utf8')


def main():
    sheets = json.loads((ROOT / 'data/edicao_2026/fichas-revisadas.json').read_text(encoding='utf8'))
    for sheet in sheets:
        for extended, folder in [(False, 'html'), (True, 'html/ext')]:
            (ROOT / folder / (sheet['html'] + '.HTML')).write_bytes(render(sheet, extended))
    print(f'Built {len(sheets)} reviewed sheets in both variants.')


if __name__ == '__main__':
    main()
