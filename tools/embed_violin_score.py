"""Embed the independently engraved violin staves; no PDF image is used."""
import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- violin-score-start -->'
END = '<!-- violin-score-end -->'


def markup():
    rows = [START, '<div class="violin-score" style="white-space:normal;color:#000;margin:18px 0 0 28px;max-width:840px">', '<b>Para violino</b>']
    for number, marker in [(1, '*'), (2, '**')]:
        path = ROOT / f'data/edicao_2026/partituras/eu-te-amo-senhor-violino-{number}.svg'
        data = base64.b64encode(path.read_bytes()).decode('ascii')
        rows.append(f'<div style="margin-top:12px"><span style="color:#FF0000">{marker}</span><img alt="Partitura para violino, trecho {marker}" style="display:block;width:100%;height:auto;background:transparent" src="data:image/svg+xml;base64,{data}"></div>')
    rows.extend(['</div>', END])
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
