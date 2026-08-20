#!/usr/bin/env python3
"""Convert the 24-bit XWD captures produced by `xwd` to PNG without extra GUI tools."""
from __future__ import annotations

import argparse
import struct
from pathlib import Path

import numpy as np
from PIL import Image


def shift_and_max(mask: int) -> tuple[int, int]:
    shift = 0
    while mask and not (mask & 1):
        shift += 1
        mask >>= 1
    return shift, mask


def convert(source: Path, target: Path) -> None:
    data = source.read_bytes()
    header = struct.unpack('>25I', data[:100])
    header_size, _, pixmap_format, _, width, height, _, byte_order, _, _, _, bits_per_pixel, bytes_per_line, _, red_mask, green_mask, blue_mask, _, _, colors, *_ = header
    if pixmap_format != 2 or bits_per_pixel not in (24, 32) or bytes_per_line != width * 4:
        raise ValueError(f'unsupported XWD layout: format={pixmap_format}, bpp={bits_per_pixel}, stride={bytes_per_line}')
    if byte_order != 0:
        raise ValueError('only MSBFirst XWD captures are supported')
    offset = header_size + colors * 12
    pixels = np.frombuffer(data, dtype='>u4', count=width * height, offset=offset).reshape(height, width)
    channels = []
    for mask in (red_mask, green_mask, blue_mask):
        shift, maximum = shift_and_max(mask)
        channels.append(((pixels & mask) >> shift) * 255 // maximum)
    rgb = np.stack(channels, axis=-1).astype(np.uint8)
    target.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgb, 'RGB').save(target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('target', type=Path)
    args = parser.parse_args()
    convert(args.source, args.target)
