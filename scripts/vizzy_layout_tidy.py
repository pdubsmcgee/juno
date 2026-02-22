#!/usr/bin/env python3
import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_pos(pos_text: str | None) -> tuple[float, float]:
    if not pos_text:
        return (0.0, 0.0)
    try:
        x_str, y_str = pos_text.split(',', 1)
        return (float(x_str), float(y_str))
    except Exception:
        return (0.0, 0.0)


def fmt_num(v: float) -> str:
    s = f"{v:.3f}".rstrip('0').rstrip('.')
    return s if s else '0'


def apply_pos_to_id(text: str, block_id: str, new_pos: str) -> str:
    pattern = re.compile(rf'<(?P<tag>[A-Za-z0-9_:-]+)(?P<attrs>[^<>]*?\bid="{re.escape(block_id)}"[^<>]*?)>')

    def repl(match: re.Match[str]) -> str:
        tag = match.group('tag')
        attrs = match.group('attrs')
        if re.search(r'\bpos="[^"]*"', attrs):
            attrs = re.sub(r'\bpos="[^"]*"', f'pos="{new_pos}"', attrs)
        else:
            if attrs.rstrip().endswith('/'):
                attrs = re.sub(r'/\s*$', f' pos="{new_pos}" /', attrs)
            else:
                attrs = attrs + f' pos="{new_pos}"'
        return f'<{tag}{attrs}>'

    return pattern.sub(repl, text, count=1)


def tidy_file(path: Path, lane_x_gap: float, block_y_gap: float, start_x: float, start_y: float) -> bool:
    raw = path.read_text(encoding='utf-8-sig')
    root = ET.fromstring(raw)

    threads: list[dict] = []
    for child in list(root):
        if child.tag != 'Instructions':
            continue
        blocks = list(child)
        if not blocks:
            continue
        first = blocks[0]
        if first.tag != 'Event':
            continue
        block_id = first.attrib.get('id')
        if not block_id:
            continue
        event_pos = parse_pos(first.attrib.get('pos'))
        threads.append({'entry_pos': event_pos, 'blocks': blocks})

    if not threads:
        return False

    threads.sort(key=lambda t: (t['entry_pos'][1], t['entry_pos'][0]))

    new_positions: dict[str, str] = {}
    for lane_idx, thread in enumerate(threads):
        base_x = start_x + lane_idx * lane_x_gap
        for block_idx, block in enumerate(thread['blocks']):
            bid = block.attrib.get('id')
            if not bid:
                continue
            x = base_x
            y = start_y + block_idx * block_y_gap
            new_positions[bid] = f"{fmt_num(x)},{fmt_num(y)}"

    updated = raw
    for bid, pos in new_positions.items():
        updated = apply_pos_to_id(updated, bid, pos)

    if updated != raw:
        path.write_text(updated, encoding='utf-8')
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description='Tidy Vizzy XML block layout into thread lanes.')
    parser.add_argument('files', nargs='+', help='XML files to tidy')
    parser.add_argument('--lane-x-gap', type=float, default=950.0)
    parser.add_argument('--block-y-gap', type=float, default=130.0)
    parser.add_argument('--start-x', type=float, default=0.0)
    parser.add_argument('--start-y', type=float, default=0.0)
    args = parser.parse_args()

    changed = 0
    for f in args.files:
        p = Path(f)
        if tidy_file(p, args.lane_x_gap, args.block_y_gap, args.start_x, args.start_y):
            changed += 1
            print(f"tidied: {p}")
        else:
            print(f"unchanged: {p}")
    print(f"files_changed={changed}")


if __name__ == '__main__':
    main()
