import json
import re
from pathlib import Path
import unittest
from build_faixa1_sheets import render

ROOT = Path(__file__).resolve().parents[1]


class Faixa1SheetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sheets = {s['html']: s for s in json.loads((ROOT/'data/edicao_2026/fichas-faixa1.json').read_text(encoding='utf8'))}

    def test_rendered_files_match_reviewed_source(self):
        for sheet in self.sheets.values():
            for extended, folder in [(False, 'html'), (True, 'html/ext')]:
                self.assertEqual((ROOT/folder/(sheet['html']+'.HTML')).read_bytes(), render(sheet, extended))

    def test_recited_repeat_has_no_invented_chord(self):
        sheet = self.sheets['ESPEREI ESPEREI NO SENHOR']
        self.assertTrue(all(not row['notes'] for row in sheet['rows'][25:30]))
        normal = render(sheet, False).decode('utf8')
        extended = render(sheet, True).decode('utf8')
        self.assertEqual(normal.count(' BIS A.'), 2)
        self.assertNotIn('NÃO QUISESTE ...', normal)
        self.assertIn('<b>NÃO QUISESTE SACRIFÍCIO NEM OBLAÇÃO,</b>', extended)
        lines = extended.splitlines()
        index = next(i for i, line in enumerate(lines) if '<b>NÃO QUISESTE SACRIFÍCIO NEM OBLAÇÃO,</b>' in line)
        self.assertEqual(lines[index - 1], '<FONT COLOR="#FF0000">')

    def test_children_bis_and_solo_response_split(self):
        child = self.sheets['ALELUIA BENDIZEI O SENHOR']
        self.assertEqual(render(child, False).decode('utf8').count(' BIS A.'), 1)
        self.assertNotIn(' BIS', render(child, True).decode('utf8'))
        song = render(self.sheets['COMO E MARAVILHOSO'], False).decode('utf8')
        self.assertNotIn('DoRe7Sol', song)
        self.assertIn('S.  Maravilhoso', song)
        self.assertIn('A.  <b>MARAVILHOSO ESTAR COM OS IRMÃOS.</b>', song)


if __name__ == '__main__':
    unittest.main()
