"""Inline original SVGs in separate ink/chord layers inheriting app font colors."""
import copy
import html
import re
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')


def themed_svg(svg, label, width=None):
    svg = re.sub(r'<\?xml[^>]*\?>', '', svg).strip()
    svg = re.sub(r'\bcolor="black"', 'color="inherit"', svg)
    svg = re.sub(r'\b(fill|stroke)="(?:black|#000000|#000)"', r'\1="currentColor"', svg, flags=re.I)
    svg = re.sub(r'stroke="(?:#999|#555)"', 'stroke="currentColor" stroke-opacity="0.55"', svg)
    root = ET.fromstring(svg)
    def red_text(node):
        return node.tag.endswith('}text') and any(n.get('fill', '').lower() in ('#ff0000', '#d92d36') for n in node.iter())
    selected = {id(n) for n in root.iter() if red_text(n)}
    ink = copy.deepcopy(root)
    for parent in ink.iter():
        for node in list(parent):
            if red_text(node): parent.remove(node)
    def prune(node):
        if id(node) in selected:
            cloned = copy.deepcopy(node)
            for n in cloned.iter():
                if 'fill' in n.attrib: n.set('fill', 'currentColor')
            return cloned
        descendants = [prune(n) for n in node]
        descendants = [n for n in descendants if n is not None]
        if not descendants: return None
        cloned = ET.Element(node.tag, dict(node.attrib))
        cloned.extend(descendants)
        return cloned
    chords = prune(root)
    ink.set('class', 'song-artwork song-artwork-ink')
    ink.set('role', 'img'); ink.set('aria-label', label); ink.set('fill', 'currentColor')
    ink.set('style', 'display:block;width:100%;height:auto')
    first = ET.tostring(ink, encoding='unicode')
    second = ''
    if chords is not None:
        # Distinct IDs prevent the overlapping layer from referring to ink definitions.
        for n in chords.iter():
            if 'id' in n.attrib: n.set('id', n.get('id')+'-chords')
        chords.set('class', 'song-artwork song-artwork-chords')
        chords.set('aria-hidden', 'true'); chords.set('fill', 'currentColor')
        chords.set('style', 'display:block;position:absolute;inset:0;width:100%;height:auto;pointer-events:none')
        second = '<font color="#FF0000">'+ET.tostring(chords, encoding='unicode')+'</font>'
    size = f'{width}px' if width else '100%'
    return '<span class="song-artwork-frame" style="display:block;position:relative;width:'+size+';max-width:100%"><font color="#000000">'+first+'</font>'+second+'</span>'
