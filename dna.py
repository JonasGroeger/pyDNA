#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

import svgwrite

ALLOWED = 'CTGA'

Y_OFFSET = 50
X_OFFSET = 50
BASE_HEIGHT = 50
BASE_WIDTH = 50
Y_HEIGHT = {
    'C': Y_OFFSET + 0 * BASE_HEIGHT,
    'T': Y_OFFSET + 1 * BASE_HEIGHT,
    'G': Y_OFFSET + 2 * BASE_HEIGHT,
    'A': Y_OFFSET + 3 * BASE_HEIGHT,
}
COLORS = {
    'C': svgwrite.rgb(178, 110, 96),
    'T': svgwrite.rgb(175, 255, 25),
    'G': svgwrite.rgb(255, 42, 0),
    'A': svgwrite.rgb(20, 78, 204),
}


def print_usage():
    print('Usage: ./dna.py <[{}]+>'.format(ALLOWED))


def check_invalid_base(sequence):
    for i, s in enumerate(sequence):
        if s not in list(ALLOWED):
            return i

    return None


def draw(sequence):

    # Base image
    svg_size_width = X_OFFSET + (len(sequence) - 1) * BASE_WIDTH + X_OFFSET
    svg_size_height = Y_OFFSET + (len(ALLOWED) - 1) * BASE_HEIGHT + Y_OFFSET
    svg = svgwrite.Drawing(sequence + '.svg', (svg_size_width, svg_size_height),
                           profile='tiny', debug=True)

    # Background
    svg.add(svg.rect(
        insert=(0, 0),
        size=('100%', '100%'),
        rx=None,
        ry=None,
        fill='rgb(255,255,255)',
    ))

    for i, base in enumerate(sequence):

        # X values
        x_begin = X_OFFSET + i * BASE_WIDTH
        x_end = x_begin + BASE_WIDTH

        # Y values
        y_begin = Y_HEIGHT[base]
        try:
            y_end = Y_HEIGHT[sequence[i+1]]
        except IndexError:
            # No line
            y_end = y_begin
            x_end = x_begin

        # Line
        svg.add(svg.line(
            (x_begin, y_begin),
            (x_end, y_end),
            stroke=svgwrite.rgb(0, 0, 0),
            stroke_width=2,
        ))

        # Area underneath
        svg.add(svg.polygon(
            points=[
                (x_begin, y_begin),
                (x_end, y_end),
                (x_end, Y_HEIGHT['A']),
                (x_begin, Y_HEIGHT['A']),
                (x_begin, y_begin),
            ],
            fill=COLORS[base],
        ))

        # Base text
        svg.add(svg.text(
            base,
            insert=(x_begin + 20, Y_HEIGHT['A'] + 25),
            fill='black',
        ))

    svg.save()


if __name__ == '__main__':

    # No arguments
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    sequence = sys.argv[1].strip()

    # Argument too short or spaces only
    if not (len(sequence) > 0):
        print('Input must be a a DNA sequence.')
        print_usage()
        sys.exit(2)

    # Contains invalid base
    invalid_base = check_invalid_base(sequence)
    if invalid_base is not None:
        print('Invalid base {}: {}'.format(sequence[invalid_base], sequence))
        print('^'.rjust(17 + invalid_base))
        print_usage()
        sys.exit(3)

    # Draw
    draw(sequence)

    print('Wrote {}.svg'.format(sequence))