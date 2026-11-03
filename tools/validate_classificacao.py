"""Check generated categories, liturgical filters and HTML colors against the reviewed 2026 manifest."""
import base64
import json
from pathlib import Path
import re
import sys


LEGACY_FLAGS = {'adve', 'laud', 'entr', 'nata', 'quar', 'pasc', 'pent', 'virg', 'cria', 'cpaz', 'fpao', 'comu', 'cfin'}


def validate_categories(document, repo):
    errors = []
    source = json.loads((repo / 'data/edicao_2026/categorias.json').read_text(encoding='utf8'))
    manifest = json.loads((repo / 'docs/revisao/classificacao-2026.json').read_text(encoding='utf8'))
    expected_catalog = [{k: c[k] for k in ('id', 'nome', 'ordem')} for c in source]
    if document.get('edicao') != 2026 or document.get('categorias') != expected_catalog:
        errors.append('Edition/category definitions differ from the reviewed 2026 catalog')
    ids = [c['id'] for c in source]
    if len(ids) != len(set(ids)) or len(ids) != 10:
        errors.append('Category IDs must be unique and contain the ten 2026 groups')
    for song in document['cantos']:
        key = song['html']
        actual = song.get('categorias', [])
        expected = [c['id'] for c in source if any(row['html'] == key and row['group'] == c['grupoFonte'] for row in manifest['liturgicalIndex'])]
        if actual != expected or len(actual) != len(set(actual)):
            errors.append(f'{key}: category memberships differ from the 2026 liturgical index')
        if LEGACY_FLAGS & set(song):
            errors.append(f'{key}: legacy boolean flags remain')
    if sum(len(s.get('categorias', [])) for s in document['cantos']) != 260:
        errors.append('Expected 260 liturgical category memberships')
    return errors


def validate(repo):
    manifest = json.loads((repo / 'docs/revisao/classificacao-2026.json').read_text(encoding='utf8'))
    songs = json.loads((repo / 'cantos.json').read_text(encoding='utf8'))['cantos']
    document = json.loads((repo / 'cantos.json').read_text(encoding='utf8'))
    errors = validate_categories(document, repo)
    expected = manifest['catalog']
    if {s['html'] for s in songs} != set(expected):
        errors.append('Catalog keys differ from the reviewed classification')
    for song in songs:
        key = song['html']
        if key not in expected:
            continue
        target = expected[key]
        for field, value in {'categoria': target['categoria']}.items():
            if song.get(field) != value:
                errors.append(f'{key}: unexpected {field}: {song.get(field)!r}, expected {value!r}')
        for field in ['html_base64', 'ext_base64']:
            html = base64.b64decode(song[field]).decode('utf8')
            color = re.search(r'background-color:\s*(#[0-9a-fA-F]{6});', html)
            if not color or color[1].upper() != target['color'].upper():
                errors.append(f'{key}/{field}: background differs from category color')
    return errors


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    problems = validate(root)
    for error in problems:
        print(error, file=sys.stderr)
    if problems:
        raise SystemExit(1)
    print('2026 classification, liturgical filters and both HTML colors validated for the current catalog.')
