"""Validate coverage and the exact reviewed treatment lines without editing HTML."""
import collections
import html
import json
from pathlib import Path
import re
import sys


def visible(line):
    return html.unescape(re.sub('<[^>]*>', '', line)).strip()


def validate(repo):
    manifest = json.loads((repo / 'docs/revisao/tratamento-2026.json').read_text(encoding='utf8'))
    catalog = json.loads((repo / 'cantos.json').read_text(encoding='utf8'))['cantos']
    keys = {s['html'] for s in catalog}
    coverage = manifest['coverage']
    errors = []
    if len(coverage) != len(catalog) or {r['html'] for r in coverage} != keys:
        errors.append('Treatment coverage does not match the complete catalog')
    for row in coverage:
        if not row['normalExamined'] or not row['extendedExamined']:
            errors.append(f'{row["html"]}: missing variant coverage')
    for row in manifest['changes']:
        folder = 'html' if row['variant'] == 'normal' else 'html/ext'
        path = repo / folder / (row['html'] + '.HTML')
        actual = collections.Counter(visible(line) for line in path.read_text(encoding='utf8').splitlines()
                                     if line.startswith('<FONT COLOR="#000000">'))
        expected = collections.Counter(e['after'] for e in row['edits'])
        for text, count in expected.items():
            if actual[text] < count:
                errors.append(f'{row["html"]}/{row["variant"]}: reviewed line missing: {text}')
        for text in {e['before'] for e in row['edits']} - set(expected):
            if actual[text]:
                errors.append(f'{row["html"]}/{row["variant"]}: uncorrected old line remains: {text}')
    return errors


if __name__ == '__main__':
    errors = validate(Path(__file__).resolve().parents[1])
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        raise SystemExit(1)
    print('Treatment coverage of the current catalog and all reviewed treatment lines validated.')
