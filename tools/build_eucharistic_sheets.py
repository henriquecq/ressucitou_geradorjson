"""Build the two complete 2026 Eucharistic prayer transcriptions, without reading a PDF."""
import copy
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def lyric_markup(row):
    text = row['text']
    highlighted = {index for index, _ in row.get('inlineRed', [])}
    parts = []
    for index, char in enumerate(text):
        encoded = html.escape(char, quote=False)
        if index in highlighted:
            encoded = '<span style="color:#FF0000">' + encoded + '</span>'
        parts.append(encoded)
    text = ''.join(parts)
    if row.get('bold'):
        text = '<b>' + text + '</b>'
    if row.get('recited'):
        text = '<i>' + text + '</i>'
    prefix = row.get('role', '').ljust(4) if row.get('role') else (' ' * 4 if row.get('bold') else ' ' * 4)
    return prefix + text


def note_markup(row):
    value = ''
    for col, note in row.get('notes', []):
        target = max(col + 4, len(value) + (1 if value else 0))
        value += ' ' * (target - len(value)) + note
    return value


def render(sheet, extended=False):
    rows = copy.deepcopy(sheet['rows'])
    if extended:
        for start, end, _ in reversed(sheet.get('repeatBlocks', [])):
            block = copy.deepcopy(rows[start:end])
            block[0]['role'] = 'A.'
            block[0]['blankBefore'] = True
            rows[end:end] = block
    header = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><style>body{margin:0px;-webkit-user-select: none;} .inv{display:none} h1{margin:0px;} .html_canto{font-size:12px;padding-left:5px;white-space:pre;font-family:monospace;} </style></head>'
    lines = [header, '<body class="html_canto" style="background-color: '+sheet['color']+';"><div>',
             '<FONT COLOR="#FF0000"><H1><b>'+html.escape(sheet['title'])+'</b></H1>',
             '<FONT COLOR="#000000"><b>'+html.escape(sheet['subtitle'])+'</b>', '',
             '<span class="inv">@capot@ </span>', '<span class="inv">@transp@</span>', '']
    for i, row in enumerate(rows):
        if row.get('blankBefore'):
            lines.append('')
        notes = note_markup(row)
        body = lyric_markup(row)
        color = '#FF0000' if row.get('recited') else '#000000'
        bracket = next(((start, end, label) for start, end, label in sheet.get('repeatBlocks', [])
                        if start <= i < end), None) if not extended else None
        if bracket:
            start, end, label = bracket
            width = max(max(len(rows[j]['text']) + 4, len(note_markup(rows[j]))) for j in range(start, end)) + 4
            side = '<font color="#000000">|</font>'
            suffix = '<font color="#000000"> '+html.escape(label)+'</font>' if i == start + (end-start)//2 else ''
            lines.append('<FONT COLOR="#FF0000">'+notes+' ' * (width-len(notes))+'</font>'+side+suffix)
            lines.append('<FONT COLOR="'+color+'">'+body+' ' * (width-len(row['text'])-4)+'</font>'+side)
        else:
            if notes:
                lines.append('<FONT COLOR="#FF0000">'+notes)
            if row.get('optional'):
                marker = '<span style="color:#FF0000;position:absolute;left:2px">*</span>' if not i or not rows[i-1].get('optional') else ''
                body = '<span style="position:relative;display:inline-block">'+marker+'<span style="position:absolute;left:20px;height:100%;border-left:1px solid #888"></span>'+body+'</span>'
            lines.append('<FONT COLOR="'+color+'">'+body)
    if sheet.get('footnote'):
        lines += ['', '<FONT COLOR="#000000"><div class="book-footnotes" style="white-space:pre-wrap;margin:16px 0 0 28px;font-size:12px;border-top:1px solid #aaa;padding-top:7px">'+html.escape(sheet['footnote'])+'</div>']
    lines += ['', '</div></body></html>', '']
    return '\r\n'.join(lines).encode('utf8')


def main():
    sheets = json.loads((ROOT/'data/edicao_2026/oracoes-eucaristicas.json').read_text(encoding='utf8'))
    for sheet in sheets:
        for extended, folder in [(False, 'html'), (True, 'html/ext')]:
            (ROOT/folder/(sheet['html']+'.HTML')).write_bytes(render(sheet, extended))
    print('Built both 2026 Eucharistic prayers, normal and extended.')


if __name__ == '__main__':
    main()
