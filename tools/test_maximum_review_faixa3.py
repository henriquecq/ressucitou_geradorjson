import json
from pathlib import Path
import unittest
from build_maximum_review_faixa3 import render

ROOT = Path(__file__).resolve().parents[1]


class MaximumReviewFaixa3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sheets = {s['html']: s for s in json.loads(
            (ROOT/'data/edicao_2026/fichas-revisao-maxima-faixa3.json').read_text(encoding='utf8'))}

    def test_transcriptions_reproduce_both_variants(self):
        for sheet in self.sheets.values():
            for extended, folder in [(False, 'html'), (True, 'html/ext')]:
                self.assertEqual((ROOT/folder/(sheet['html']+'.HTML')).read_bytes(), render(sheet, extended))

    def test_two_lirio_repeats_and_tonal_consistency(self):
        sheet = self.sheets['COMO LIRIO ENTRE OS ESPINHOS']
        normal, extended = render(sheet, False).decode('utf8'), render(sheet, True).decode('utf8')
        self.assertEqual(normal.count(' BIS A.'), 2)
        self.assertEqual(extended.count('<b>INTRODUZIU-ME</b>'), 2)
        self.assertEqual(extended.count('<b>E A BANDEIRA QUE DESFRALDA</b>'), 2)
        self.assertNotIn('Si-', normal)
        self.assertNotIn('Fa#', normal)

    def test_no_legacy_repetition_in_vos_or_mesmo_deus(self):
        for key in ['VOS SOIS A LUZ DO MUNDO', 'O MESMO DEUS']:
            self.assertNotIn(' BIS', render(self.sheets[key], False).decode('utf8'))
        normal = render(self.sheets['O MESMO DEUS'], False).decode('utf8')
        self.assertIn('S.  Mas levamos este tesouro', normal)
        self.assertIn('<b>MAS LEVAMOS ESTE TESOURO</b>', normal)
        self.assertIn('S.  Enquanto nós morremos', normal)
        self.assertIn('<b>ENQUANTO NÓS MORREMOS</b>', normal)

    def test_sobe_bis_returns_expand_and_amem_wisdom_uses_seventh(self):
        sheet = self.sheets['SOBE DEUS ENTRE ACLAMACOES']
        normal, extended = render(sheet, False).decode('utf8'), render(sheet, True).decode('utf8')
        self.assertEqual(normal.count(' BIS A.'), 2)
        self.assertNotIn('...', extended)
        self.assertEqual(extended.count('<b>SOBE DEUS ENTRE ACLAMAÇÕES,</b>'), 5)
        wisdom = next(r for r in self.sheets['AMEM AMEM AMEM']['rows'] if r['text'] == 'SABEDORIA,')
        self.assertEqual(wisdom['notes'], [[6, 'Sol7']])


if __name__ == '__main__':
    unittest.main()
