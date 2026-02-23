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


def tidy_file(
    path: Path,
    lane_x_gap: float,
    block_y_gap: float,
    start_x: float | None,
    start_y: float | None,
    lanes_per_row: int,
    row_y_gap: float,
) -> bool:
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

    # Keep layout anchored near the previous visible region when explicit
    # starts are not provided. This avoids moving all code far from the
    # current viewport after a pretty pass.
    if start_x is None:
        start_x = min(t['entry_pos'][0] for t in threads)
    if start_y is None:
        start_y = min(t['entry_pos'][1] for t in threads)

    # Wrap lanes into rows so large programs stay near the initial viewport.
    lanes_per_row = max(1, lanes_per_row)
    row_heights: list[float] = []
    for row_start in range(0, len(threads), lanes_per_row):
        row_threads = threads[row_start:row_start + lanes_per_row]
        tallest = max(len(t['blocks']) for t in row_threads)
        row_heights.append(max(1.0, (tallest - 1) * block_y_gap + row_y_gap))

    row_offsets: list[float] = []
    acc = 0.0
    for h in row_heights:
        row_offsets.append(acc)
        acc += h

    new_positions: dict[str, str] = {}
    for lane_idx, thread in enumerate(threads):
        row_idx = lane_idx // lanes_per_row
        col_idx = lane_idx % lanes_per_row
        base_x = start_x + col_idx * lane_x_gap
        base_y = start_y + row_offsets[row_idx]
        for block_idx, block in enumerate(thread['blocks']):
            bid = block.attrib.get('id')
            if not bid:
                continue
            x = base_x
            y = base_y + block_idx * block_y_gap
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
    parser.add_argument('--start-x', type=float, default=None)
    parser.add_argument('--start-y', type=float, default=None)
    parser.add_argument('--lanes-per-row', type=int, default=4)
    parser.add_argument('--row-y-gap', type=float, default=260.0)
    args = parser.parse_args()

    changed = 0
    for f in args.files:
        p = Path(f)
        if tidy_file(p, args.lane_x_gap, args.block_y_gap, args.start_x, args.start_y, args.lanes_per_row, args.row_y_gap):
            changed += 1
            print(f"tidied: {p}")
        else:
            print(f"unchanged: {p}")
    print(f"files_changed={changed}")


if __name__ == '__main__':
    main()
