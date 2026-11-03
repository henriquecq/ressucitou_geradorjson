"""Render the complete 2026 versions of the explicitly transcribed complementary sheets."""
import copy
import html
import json
from pathlib import Path
from build_reviewed_sheets import line_markup

ROOT = Path(__file__).resolve().parents[1]


def render(sheet, extended):
    header = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><style>body{margin:0px;-webkit-user-select:none;} .inv{display:none} h1{margin:0px;} .html_canto{font-size:12px;padding-left:5px;white-space:pre;font-family:monospace;}</style></head>'
    result = [header, '<body class="html_canto" style="background-color: '+sheet['color']+';"><div>',
              '<FONT COLOR="#FF0000"><H1><b>'+html.escape(sheet['title'])+'</b></H1>',
              '<FONT COLOR="#000000"><b>'+html.escape(sheet['subtitle'])+'</b>', '',
              '<span class="inv">@capot@ </span>'+html.escape(sheet.get('capo','')),
              '<span class="inv">@transp@</span>', '']
    for i, row in enumerate(sheet['rows']):
        rows = [row]
        expansion = sheet['expansions'].get(str(i)) if extended else None
        if expansion:
            rows = copy.deepcopy(sheet['rows'][expansion[0]:expansion[1]])
            rows[0]['role'] = row['role']
            if row['notes'] and row['notes'][0][0] == 0 and not any(col == 0 for col,note in rows[0]['notes']):
                rows[0]['notes'].insert(0, row['notes'][0])
        for entry in rows:
            if entry.get('role'):
                result.append('')
            result.extend(line_markup(entry))
    result += ['', '</div></body></html>', '']
    return '\r\n'.join(result).encode('utf8')


def main():
    for sheet in json.loads((ROOT/'data/edicao_2026/fichas-complementares.json').read_text(encoding='utf8')):
        for extended, folder in [(False,'html'),(True,'html/ext')]:
            (ROOT/folder/(sheet['html']+'.HTML')).write_bytes(render(sheet,extended))


if __name__ == '__main__':
    main()
