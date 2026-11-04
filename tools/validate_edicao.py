"""Validate the 2026 active/retired inventory and reviewed sheet generation."""
import json
from pathlib import Path
import sys
from build_reviewed_sheets import render
from build_eucharistic_sheets import render as render_eucharistic
from build_complementary_sheets import render as render_complementary
from build_faixa1_sheets import render as render_faixa1
from build_maximum_review_faixa3 import render as render_faixa3
from build_pente_fino_faixa2 import render as render_pente_fino
from embed_violin_score import markup as violin_markup, START as VIOLIN_START, END as VIOLIN_END
from build_litany_ii import render as render_litany


def validate(root):
    policy = json.loads((root / 'data/edicao_2026/catalogo.json').read_text(encoding='utf8'))
    catalog = json.loads((root / 'cantos.json').read_text(encoding='utf8'))['cantos']
    reviewed = json.loads((root / 'data/edicao_2026/fichas-revisadas.json').read_text(encoding='utf8'))
    by_key = {song['html']: song for song in catalog}
    errors = []
    litany = json.loads((root / 'data/edicao_2026/ladainha-penitencial-ii.json').read_text(encoding='utf8'))
    for extended, folder in [(False, 'html'), (True, 'html/ext')]:
        if (root / folder / 'LADAINHA PENITENCIAL II.HTML').read_bytes() != render_litany(litany, extended):
            errors.append(f'LADAINHA PENITENCIAL II/{folder}: differs from approved presentation')
    for folder in ['html', 'html/ext']:
        source = (root / folder / 'EU TE AMO SENHOR.HTML').read_text(encoding='utf8')
        expected = violin_markup().replace('\r\n', '\n')
        if source.count(VIOLIN_START) != 1 or source.count(VIOLIN_END) != 1 or expected not in source:
            errors.append(f'EU TE AMO SENHOR/{folder}: original violin engraving differs from SVG sources')
    for filename, renderer in [('oracoes-eucaristicas.json', render_eucharistic),
                               ('fichas-complementares.json', render_complementary),
                               ('fichas-faixa1.json', render_faixa1),
                               ('fichas-revisao-maxima-faixa3.json', render_faixa3),
                               ('fichas-pente-fino-2-faixa2.json', render_pente_fino)]:
        sheets = json.loads((root / 'data/edicao_2026' / filename).read_text(encoding='utf8'))
        for sheet in sheets:
            for extended, folder in [(False, 'html'), (True, 'html/ext')]:
                path = root / folder / (sheet['html'] + '.HTML')
                if path.read_bytes() != renderer(sheet, extended):
                    errors.append(f'{sheet["html"]}/{folder}: differs from complete 2026 transcription')
    output_pages = [int(song['numero']) for song in catalog]
    if output_pages != sorted(output_pages):
        errors.append('Catalog order differs from the 2026 book order')
    if set(by_key) != set(policy['active']):
        errors.append('Active catalog differs from edition inventory')
    for key, metadata in policy['active'].items():
        song = by_key.get(key, {})
        obsolete = {'nr_2019', 'nr_2026', 'conteudo'} & set(song)
        if obsolete:
            errors.append(f'{key}: obsolete JSON fields remain: {sorted(obsolete)}')
        if song.get('numero') != str(metadata['page']):
            errors.append(f'{key}: 2026 page differs')
        if metadata.get('title') and song.get('titulo') != metadata['title']:
            errors.append(f'{key}: current display title differs')
        if metadata.get('newId') is not None and song.get('id') != metadata['newId']:
            errors.append(f'{key}: new ID differs from edition inventory')
    for row in policy['retired']:
        if row['html'] in by_key:
            errors.append(f'{row["html"]}: retired entry still active')
        for folder in ['html', 'html/ext']:
            if not (root / folder / (row['html'] + '.HTML')).is_file():
                errors.append(f'{row["html"]}: historical source lost')
    if by_key.get('CANTAI A DEUS', {}).get('id') != 45:
        errors.append('Cantai a Deus historical ID 45 was not preserved')
    for sheet in reviewed:
        for extended, folder, label in [(False, 'html', 'normal'), (True, 'html/ext', 'estendida')]:
            path = root / folder / (sheet['html'] + '.HTML')
            if path.read_bytes() != render(sheet, extended):
                errors.append(f'{sheet["html"]}/{label}: differs from reviewed transcription')
            archive = root / 'html/legado/ate-2025' / label / (sheet['html'] + '.HTML')
            if sheet.get('legacyArchive', True) and not archive.is_file():
                errors.append(f'{sheet["html"]}/{label}: previous HTML not archived')
    pages = [row['page'] for row in policy['active'].values()] + [r['page'] for r in policy['missingSheets']]
    if len(pages) != policy['targetSheetCount'] or len(set(pages)) != len(pages):
        errors.append('The book sheet inventory has gaps or duplicate mappings')
    return errors


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        raise SystemExit(1)
    print('2026 edition inventory, historical files and reviewed transcriptions validated.')
