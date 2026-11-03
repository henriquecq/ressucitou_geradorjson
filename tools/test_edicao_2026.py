import copy
import json
from pathlib import Path
import unittest
from validate_catalog import validate_catalog
from build_reviewed_sheets import render
from validate_classificacao import validate_categories

ROOT = Path(__file__).resolve().parents[1]


class Edition2026Tests(unittest.TestCase):
    def test_repeat_blocks_have_side_brackets_only_in_normal_variant(self):
        import re
        for sheet in self.sheets.values():
            if not sheet.get('repeatBlocks'):
                continue
            normal = render(sheet, False).decode('utf8')
            extended = render(sheet, True).decode('utf8')
            self.assertEqual(normal.count(' BIS'), len(sheet['repeatBlocks']))
            self.assertNotIn(' BIS', extended)
            for line in normal.splitlines():
                if ' BIS' in line:
                    self.assertIn('|', re.sub('<[^>]*>', '', line))

    def test_dynamic_categories_match_the_book(self):
        document = json.loads((ROOT / 'cantos.json').read_text(encoding='utf8'))
        self.assertEqual(validate_categories(document, ROOT), [])
        for invalid in ('unknown-category', 'pascoa-pentecostes'):
            modified = copy.deepcopy(document)
            modified['cantos'][0]['categorias'].append(invalid)
            self.assertTrue(validate_categories(modified, ROOT))

    def test_removed_laudes_category_and_legacy_flags_cannot_return(self):
        document = json.loads((ROOT / 'cantos.json').read_text(encoding='utf8'))
        document['categorias'].append({'id': 'laudes', 'nome': 'Laudes - Vésperas', 'ordem': 11})
        document['cantos'][0]['laud'] = True
        self.assertTrue(validate_categories(document, ROOT))

    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / 'cantos.json').read_text(encoding='utf8'))['cantos']
        cls.policy = json.loads((ROOT / 'data/edicao_2026/catalogo.json').read_text(encoding='utf8'))
        cls.sheets = {s['html']: s for s in json.loads((ROOT / 'data/edicao_2026/fichas-revisadas.json').read_text(encoding='utf8'))}

    def test_unapproved_disappearance_is_rejected(self):
        removed = self.catalog[0]['html']
        errors = validate_catalog(self.catalog[1:], self.catalog,
                                  {r['html']: r['id'] for r in self.policy['retired']})
        self.assertTrue(any(removed in error and 'removed' in error for error in errors))

    def test_existing_id_change_is_rejected(self):
        modified = copy.deepcopy(self.catalog)
        modified[0]['id'] = 999999
        self.assertTrue(any('existing ID changed' in e for e in validate_catalog(modified, self.catalog)))

    def test_extended_responsorial_psalm_contains_four_full_refrains(self):
        sheet = self.sheets['SALMODIA PARA O SALMO RESPONSORIAL']
        normal, extended = render(sheet, False).decode('utf8'), render(sheet, True).decode('utf8')
        opening = '<b>SOIS VÓS, Ó SENHOR,</b>'
        self.assertEqual(normal.count(opening), 1)
        self.assertEqual(extended.count(opening), 4)
        self.assertNotIn('BIS A.', extended)
        self.assertNotIn('SENHOR, ...', extended)

    def test_cantai_uses_historical_id_and_expands_bis_and_final_return(self):
        song = next(s for s in self.catalog if s['html'] == 'CANTAI A DEUS')
        self.assertEqual(song['id'], 45)
        extended = render(self.sheets['CANTAI A DEUS'], True).decode('utf8')
        self.assertEqual(extended.count('<b>CANTAI A DEUS,</b>'), 6)
        self.assertNotIn('BIS A.', extended)

    def test_new_long_refrains_are_expanded_completely(self):
        expectations = {
            'ALEGRIA NASCEU O SALVADOR': ('<b>ALEGRIA, ALEGRIA, ALEGRIA,</b>', 6),
            'SEQUENCIA DE CORPUS CHRISTI': ('<b>TERRA, EXULTA DE ALEGRIA,</b>', 6),
            'SUBA O ESPOSO AO LENHO DO SEU TALAMO': ('<b>SUBA O ESPOSO,</b>', 4),
            'ONDE TE ESCONDESTE AMADO': ('<b>MIL GRAÇAS DERRAMANDO,</b>', 2),
        }
        for key, (opening, count) in expectations.items():
            with self.subTest(song=key):
                extended = render(self.sheets[key], True).decode('utf8')
                self.assertEqual(extended.count(opening), count)
                self.assertNotIn('BIS A.', extended)
        self.assertEqual(render(self.sheets['SUBA O ESPOSO AO LENHO DO SEU TALAMO'], True)
                         .decode('utf8').count('Braçadeira 3º Traste'), 1)

    def test_book_inventory_is_complete_and_new_ids_do_not_reuse_retired_ids(self):
        self.assertEqual(len(self.catalog), 236)
        self.assertEqual(self.policy['missingSheets'], [])
        pages = [int(song['numero']) for song in self.catalog]
        self.assertEqual(pages, sorted(pages))
        retired_ids = {r['id'] for r in self.policy['retired']}
        for metadata in self.policy['active'].values():
            if 'newId' in metadata:
                self.assertNotIn(metadata['newId'], retired_ids)

    def test_current_json_uses_only_numero_for_the_2026_page(self):
        obsolete = {'nr_2019', 'nr_2026', 'conteudo'}
        for song in self.catalog:
            with self.subTest(song=song['html']):
                self.assertFalse(obsolete & set(song))
                self.assertIsInstance(song['numero'], str)
                self.assertEqual(song['numero'], str(self.policy['active'][song['html']]['page']))


if __name__ == '__main__':
    unittest.main()
