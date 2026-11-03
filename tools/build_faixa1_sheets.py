"""Reproduce four fully reviewed 2026 sheets with explicit repeat/response boundaries."""
import copy
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def row_markup(row):
    if row.get('role') == 'Crianças':
        following = copy.deepcopy(row)
        following['role'] = ''
        return ['<FONT COLOR="#000000"><b>Crianças</b>'] + row_markup(following)
    prefix = max(4, len(row.get('role', '')) + 1)
    lead = row.get('role', '').ljust(prefix) if row.get('role') else (' ' if row.get('bold') else ' ') * prefix
    notes = ''
    for col, note in row.get('notes', []):
        target = max(prefix + col, len(notes) + (1 if notes else 0))
        notes += ' ' * (target - len(notes)) + note
    text = html.escape(row['text'], quote=False)
    if row.get('bold'):
        text = '<b>' + text + '</b>'
    if row.get('melisma'):
        text += ' <font color="#FF0000"><i>(melisma)</i></font>'
    return ['<FONT COLOR="#FF0000">' + notes, '<FONT COLOR="#000000">' + lead + text]


def bracket(rows, label):
    lines = [line for row in rows for line in row_markup(row)]
    bracketed = [i for i, line in enumerate(lines) if line != '<FONT COLOR="#000000"><b>Crianças</b>']
    width = max(len(html.unescape(re.sub('<[^>]*>', '', lines[i]))) for i in bracketed) + 4
    for i, line in enumerate(lines):
        if i not in bracketed:
            continue
        length = len(html.unescape(re.sub('<[^>]*>', '', line)))
        lines[i] = line + ' ' * (width - length) + '</font><font color="#000000">|</font>'
        if i == bracketed[len(bracketed) // 2]:
            lines[i] += '<font color="#000000"> ' + html.escape(label) + '</font>'
    return lines


def render(sheet, extended):
    result = ['<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><style>body{margin:0px;-webkit-user-select:none;} .inv{display:none} h1{margin:0px;} .html_canto{font-size:12px;padding-left:5px;white-space:pre;font-family:monospace;}</style></head>',
              '<body class="html_canto" style="background-color: '+sheet['color']+';"><div>',
              '<FONT COLOR="#FF0000"><H1><b>'+html.escape(sheet['title'])+'</b></H1>',
              '<FONT COLOR="#000000"><b>'+html.escape(sheet['subtitle'])+'</b>', '',
              '<span class="inv">@capot@ </span>'+html.escape(sheet.get('capo', '')),
              '<span class="inv">@transp@</span>', '']
    starts = {start: (end, label) for start, end, label in sheet.get('repeatBlocks', [])}
    i = 0
    while i < len(sheet['rows']):
        if extended and i in sheet.get('skipRowsExtended', []):
            i += 1
            continue
        row = sheet['rows'][i]
        if i in starts:
            end, label = starts[i]
            block = sheet['rows'][i:end]
            result.append('')
            if not extended:
                result.extend(bracket(block, label))
            else:
                for item in block:
                    result.extend(row_markup(item))
                response = copy.deepcopy(block)
                response[0]['role'] = 'A.'
                if sheet.get('plainRepeatResponse'):
                    for item in response:
                        item['bold'] = True
                        item['text'] = item['text'].upper()
                result.append('')
                for item in response:
                    result.extend(row_markup(item))
            i = end
            continue
        expansion = sheet.get('expansions', {}).get(str(i)) if extended else None
        if expansion:
            block = copy.deepcopy(sheet['rows'][expansion[0]:expansion[1]])
            block[0]['role'] = row.get('role', 'A.')
            if sheet.get('repeatExpandedCalls') and expansion == [0, 2]:
                block += copy.deepcopy(block)
        else:
            block = [row]
        for item in block:
            if item.get('role'):
                result.append('')
            result.extend(row_markup(item))
        i += 1
    if sheet.get('footnote'):
        result += ['', '<FONT COLOR="#000000"><div class="book-footnotes" style="white-space:pre-wrap;margin:16px 0 0 28px;font-size:12px;border-top:1px solid #aaa;padding-top:7px">'+html.escape(sheet['footnote'])+'</div>']
    result += ['', '</div></body></html>', '']
    return '\r\n'.join(result).encode('utf8')


def main():
    for sheet in json.loads((ROOT/'data/edicao_2026/fichas-faixa1.json').read_text(encoding='utf8')):
        for extended, folder in [(False, 'html'), (True, 'html/ext')]:
            (ROOT/folder/(sheet['html']+'.HTML')).write_bytes(render(sheet, extended))


if __name__ == '__main__':
    main()
