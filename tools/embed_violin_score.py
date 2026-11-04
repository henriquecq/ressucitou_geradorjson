"""Embed the independently engraved violin staves; no PDF image is used."""
import re
from pathlib import Path
from themed_svg import themed_svg

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- violin-score-start -->'
END = '<!-- violin-score-end -->'


def markup():
    rows = [START, '<FONT COLOR="#000000"><div class="violin-score" style="white-space:normal;margin:18px 0 0 28px;max-width:840px">', '<b>Para violino</b>']
    for number, marker in [(1, '*'), (2, '**')]:
        path = ROOT / f'data/edicao_2026/partituras/eu-te-amo-senhor-violino-{number}.svg'
        svg = themed_svg(path.read_text(encoding='utf8'), 'Partitura para violino, trecho '+marker)
        rows.append(f'<div style="margin-top:12px"><font color="#FF0000">{marker}</font>'+svg+'</div>')
    rows.extend(['</div></font>', END])
    return '\r\n'.join(rows)


def main():
    for folder in ['html', 'html/ext']:
        path = ROOT / folder / 'EU TE AMO SENHOR.HTML'
        source = path.read_text(encoding='utf8').replace('\r\n', '\n')
        block = markup().replace('\r\n', '\n')
        if START in source:
            source = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda _: block, source, flags=re.S)
        else:
            source = source.replace('</div></body></html>', block + '\n</div></body></html>')
        path.write_bytes(source.replace('\n', '\r\n').encode('utf8'))


if __name__ == '__main__':
    main()
