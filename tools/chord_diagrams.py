"""Render original, schematic guitar diagrams from string/fret facts (no PDF assets)."""
import base64
import html


def diagram_svg(diagram):
    label=html.escape(diagram['label'])
    dots=diagram['dots']
    if any(not (isinstance(s,int) and isinstance(f,int) and 0<=s<6 and 1<=f<=7) for s,f in dots):
        raise ValueError('Invalid string/fret coordinate')
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="190" height="124" viewBox="0 0 190 124">',
           '<title>Diagrama de '+label+'</title>',
           '<text x="40" y="20" fill="#d92d36" font-family="Arial,sans-serif" font-size="15" font-weight="bold">'+label+'</text>']
    for s in range(6):
        y=36+s*14
        parts.append(f'<path d="M36 {y}H176" stroke="#999" stroke-width="1"/>')
    for f in range(8):
        x=36+f*20
        parts.append(f'<path d="M{x} 36V106" stroke="'+('black' if f==0 else '#999')+'" stroke-width="'+('5' if f==0 else '1')+'"/>')
    for s,f in dots:
        parts.append(f'<circle cx="{26+f*20}" cy="{36+s*14}" r="4.1" fill="black"/>')
    for s in diagram.get('muted',[]):
        y=36+s*14
        parts.append(f'<path d="M22 {y-4}L30 {y+4}M30 {y-4}L22 {y+4}" stroke="#555" stroke-width="2"/>')
    parts.append('</svg>')
    return ''.join(parts)


def diagrams_markup(diagrams):
    images=[]
    for diagram in diagrams:
        uri='data:image/svg+xml;base64,'+base64.b64encode(diagram_svg(diagram).encode('utf8')).decode('ascii')
        images.append('<img alt="Diagrama de '+html.escape(diagram['label'],quote=True)+'" width="190" height="124" src="'+uri+'">')
    return '<div class="book-diagrams" style="white-space:normal;display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 0 28px">'+''.join(images)+'</div>'
