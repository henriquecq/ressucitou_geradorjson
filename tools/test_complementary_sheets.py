import json
from pathlib import Path
import unittest
from build_complementary_sheets import render

ROOT = Path(__file__).resolve().parents[1]


class ComplementarySheetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sheets = {s['html']: s for s in json.loads((ROOT/'data/edicao_2026/fichas-complementares.json').read_text(encoding='utf8'))}

    def test_reproducible_normal_and_extended(self):
        for sheet in self.sheets.values():
            for extended, folder in [(False, 'html'), (True, 'html/ext')]:
                self.assertEqual((ROOT/folder/(sheet['html']+'.HTML')).read_bytes(), render(sheet, extended))

    def test_missing_verses_and_vocalization_restored(self):
        text = render(self.sheets['MUITO ME PERSEGUIRAM'], False).decode('utf8')
        self.assertIn('S.  Sobre as minhas costas araram aradores,', text)
        self.assertIn('<b>SOBRE AS MINHAS COSTAS</b>', text)
        for extended in (False, True):
            text = render(self.sheets['POR AMOR DE MEUS AMIGOS'], extended).decode('utf8')
            self.assertEqual(text.count('<b>LA LALALALALA, LA LALALALALA</b>'), 2)

    def test_salve_response_and_extended_expansions(self):
        sheet = self.sheets['SALVE RAINHA']
        self.assertIn('<b>Ó CLEMENTE! Ó PIEDOSA! Ó DOCE, VIRGEM MARIA!</b>', render(sheet, False).decode('utf8'))
        self.assertNotIn('Amém', render(sheet, False).decode('utf8'))
        extended = render(self.sheets['POR AMOR DE MEUS AMIGOS'], True).decode('utf8')
        self.assertNotIn('...', extended)


if __name__ == '__main__':
    unittest.main()
