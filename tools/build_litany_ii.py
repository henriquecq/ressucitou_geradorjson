"""Render the user-approved normal/extended presentation of litany II."""
import json
from pathlib import Path
from build_complementary_sheets import render as render_sheet
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/edicao_2026/ladainha-penitencial-ii.json'


def render(data, extended):
    rows = []
    def row(text, role='', notes=None, bold=False):
        rows.append(dict(text=text, role=role, notes=notes or [], bold=bold))
    def kyrie():
        row('Senhor tende piedade.', 'S.', [[3, 'Do'], [17, 'Si7']])
        row('SENHOR TENDE PIEDADE', 'A.', [[3, 'Do'], [17, 'Si7']], True)
    row(data['intro'], 'S.', [[0, 'Mi-'], [len(data['intro'])-4, 'La-']])
    row(data['response'], 'A.', data['responseNotes'], True)
    kyrie()
    for group_index, group in enumerate(data['groups']):
        if not extended:
            row(data['formula'] + ' ...', 'S.', [[0, 'Mi-']] if group_index == 0 else [])
        for index, invocation in enumerate(group):
            if extended:
                row(data['formula'], 'S.', [[0, 'Mi-']] if group_index == index == 0 else [])
                row(invocation, notes=[[max(0, len(invocation)-4), 'La-']] if group_index == index == 0 else [])
                row(data['response'], 'A.', data['responseNotes'], True)
            else:
                row('- ' + invocation, 'S.' if index == 0 else '', [[max(0, len(invocation)-2), 'La-']] if group_index == index == 0 else [])
                row('TENDE PIEDADE DE MIM ...', 'A.' if index == 0 else '', [[17, 'Si7']] if group_index == index == 0 else [], True)
        kyrie()
    sheet = dict(data, rows=rows, expansions={})
    return render_sheet(sheet, False)


def main():
    data = json.loads(SOURCE.read_text(encoding='utf8'))
    for extended, folder in [(False, 'html'), (True, 'html/ext')]:
        (ROOT / folder / (data['html'] + '.HTML')).write_bytes(render(data, extended))


if __name__ == '__main__':
    main()
