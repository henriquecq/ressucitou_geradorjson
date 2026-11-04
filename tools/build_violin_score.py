"""Engrave the manually reviewed violin transcription as original SVGs.

Requires verovio 6.4.1 only when regenerating the engraving. HTML embedding
uses the committed SVGs and Python standard library. No PDF is read here.
"""
from pathlib import Path
from fractions import Fraction
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/edicao_2026/partituras/eu-te-amo-senhor-violino.json'
DURATIONS = {'w': (48, 'whole'), 'h': (24, 'half'), 'q': (12, 'quarter'), 'q.': (18, 'quarter'), 'e': (6, 'eighth'), 's': (3, '16th'), 'st': (2, '16th')}


def child(parent, tag, text=None, **attrs):
    element = ET.SubElement(parent, tag, attrs)
    if text is not None:
        element.text = str(text)
    return element


def musicxml(section):
    score = ET.Element('score-partwise', version='4.0')
    parts = child(score, 'part-list')
    child(child(parts, 'score-part', id='P1'), 'part-name', '')
    part = child(score, 'part', id='P1')
    meter = [4, 4]
    for number, entries in enumerate(section['measures'], 1):
        measure = child(part, 'measure', number=str(number))
        if number in section['systems']:
            child(measure, 'print', **{'new-system': 'yes'})
        if number == 1 or str(number) in section.get('meters', {}):
            attrs = child(measure, 'attributes')
            if number == 1:
                child(attrs, 'divisions', 12)
                child(child(attrs, 'key'), 'fifths', 2)
                clef = child(attrs, 'clef'); child(clef, 'sign', 'G'); child(clef, 'line', 2)
            meter = section.get('meters', {}).get(str(number), [4, 4])
            time = child(attrs, 'time', **({'symbol': 'common'} if meter == [4, 4] else {}))
            child(time, 'beats', meter[0]); child(time, 'beat-type', meter[1])
        chord = section['chords'].get(str(number))
        if chord:
            direction = child(measure, 'direction', placement='above')
            child(child(direction, 'direction-type'), 'words', chord, color='#FF0000', **{'font-weight': 'bold'})
        total = 0
        for index, value in enumerate(entries):
            name, rhythm = value.split(':'); duration, kind = DURATIONS[rhythm]; total += duration
            note = child(measure, 'note'); pitch = child(note, 'pitch')
            child(pitch, 'step', name[0])
            if '#' in name: child(pitch, 'alter', 1)
            child(pitch, 'octave', name[-1]); child(note, 'duration', duration)
            ties = []
            for m1, n1, m2, n2 in section.get('ties', []):
                if (number, index) == (m1, n1): ties.append('start')
                if (number, index) == (m2, n2): ties.append('stop')
            for tie in ties: child(note, 'tie', type=tie)
            child(note, 'type', kind)
            if rhythm.endswith('.'): child(note, 'dot')
            if rhythm == 'st':
                tm = child(note, 'time-modification'); child(tm, 'actual-notes', 3); child(tm, 'normal-notes', 2); child(tm, 'normal-type', '16th')
            if kind != 'whole': child(note, 'stem', 'up')
            for bar, first, last in section.get('beams', []):
                if number == bar and first <= index <= last:
                    beam_type = 'begin' if index == first else 'end' if index == last else 'continue'
                    for level in range(1, 3 if rhythm in ('s', 'st') else 2):
                        child(note, 'beam', beam_type, number=str(level))
            notations = child(note, 'notations')
            for tie in ties: child(notations, 'tied', type=tie)
            for sid, (m1, n1, m2, n2) in enumerate(section.get('slurs', [])):
                for position, typ in [((m1, n1), 'start'), ((m2, n2), 'stop')]:
                    if (number, index) == position: child(notations, 'slur', type=typ, number=str(sid % 6 + 1), placement='below')
            if rhythm == 'st' and (index == 1 or index == 3):
                child(notations, 'tuplet', type='start' if index == 1 else 'stop', bracket='no', placement='above')
            if section.get('upBow') == [number, index]: child(child(notations, 'technical'), 'up-bow')
        assert Fraction(total, 12) == Fraction(meter[0] * 4, meter[1]), (section['id'], number, total, meter)
        if number == len(section['measures']): child(child(measure, 'barline', location='right'), 'bar-style', 'light-heavy')
    return ET.tostring(score, encoding='unicode')


def main():
    import verovio
    data = json.loads(SOURCE.read_text(encoding='utf8'))
    for section in data['sections']:
        xml = musicxml(section)
        target = SOURCE.parent / ('eu-te-amo-senhor-' + section['id'])
        target.with_suffix('.musicxml').write_text(xml, encoding='utf8')
        toolkit = verovio.toolkit()
        toolkit.setOptions({'pageWidth': 2100, 'pageHeight': 1800, 'scale': 40, 'adjustPageHeight': True, 'breaks': 'encoded', 'header': 'none', 'footer': 'none', 'svgViewBox': True})
        assert toolkit.loadData(xml)
        assert toolkit.getPageCount() == 1
        svg = toolkit.renderToSVG(1, False)
        target.with_suffix('.svg').write_text(svg, encoding='utf8')
        print(target.name)


if __name__ == '__main__':
    main()
