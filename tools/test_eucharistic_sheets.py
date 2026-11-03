import json
from pathlib import Path
import unittest

from build_eucharistic_sheets import render

ROOT = Path(__file__).resolve().parents[1]


class EucharisticSheetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sheets = {s['html']: s for s in json.loads(
            (ROOT/'data/edicao_2026/oracoes-eucaristicas.json').read_text(encoding='utf8'))}

    def test_generated_variants_are_reproducible(self):
        for sheet in self.sheets.values():
            for extended, folder in [(False, 'html'), (True, 'html/ext')]:
                self.assertEqual((ROOT/folder/(sheet['html']+'.HTML')).read_bytes(), render(sheet, extended))

    def test_prayer_ii_restores_missing_2026_passages(self):
        sheet = self.sheets['ORACAO EUCARISTICA II']
        text = ' '.join(r['text'] for r in sheet['rows'])
        for required in ['por vosso amado Filho, Jesus Cristo.',
                         'e adquirir para vós um povo santo,',
                         'pronunciou a bênção de ação de graças,',
                         'os bispos do mundo inteiro, os presbíteros,',
                         'e todos os Santos que neste mundo viveram na vossa amizade,',
                         'por todos os séculos dos séculos.']:
            self.assertIn(required, text)
        recited = [r['text'] for r in sheet['rows'] if r.get('recited') and not r.get('rubric')]
        self.assertIn('Na verdade, ó Pai, vós sois santo, fonte de toda santidade.', recited)
        self.assertEqual(len(recited), 4)
        self.assertEqual(sum(r.get('optional', False) for r in sheet['rows']), 2)

    def test_prayer_iv_restores_missing_2026_passages(self):
        sheet = self.sheets['ORACAO EUCARISTICA IV']
        text = ' '.join(r['text'] for r in sheet['rows'])
        for required in ['Criastes o ser humano à vossa imagem',
                         'à família humana e a instruístes',
                         'que continua sua obra no mundo para levar à plenitude toda a santificação.',
                         'Jesus tomou o pão, pronunciou a bênção de ação de graças, partiu',
                         'nos tornemos em Cristo uma oferenda viva',
                         'os diáconos, e todos os ministros da vossa Igreja,']:
            self.assertIn(required, text)
        self.assertEqual(sheet['subtitle'], '(1988)')

    def test_normal_bis_has_bracket_and_extended_has_full_repeat(self):
        for sheet in self.sheets.values():
            normal, extended = render(sheet, False).decode('utf8'), render(sheet, True).decode('utf8')
            self.assertEqual(normal.count(' BIS'), len(sheet['repeatBlocks']))
            self.assertNotIn(' BIS', extended)
            for start, end, _ in sheet['repeatBlocks']:
                for row in sheet['rows'][start:end]:
                    token = '<b>'+row['text']+'</b>'
                    self.assertEqual(extended.count(token), 2)


if __name__ == '__main__':
    unittest.main()
