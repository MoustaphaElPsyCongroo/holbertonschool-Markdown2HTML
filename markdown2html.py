#!/usr/bin/python3
"""Markdown to html parser"""
from sys import argv, exit
import re

argslen = len(argv) - 1


def main():
    if argslen < 2:
        exit('Usage: ./markdown2html.py README.md README.html')

    md_file = argv[1]
    html_file = argv[2]
    try:
        with open(md_file, 'r', encoding='utf-8') as md:
            with open(html_file, 'w', encoding='utf-8') as html:
                multilines = ('- ', '* ')
                converted = None
                items = {
                    'type': None,
                    'elems': []
                }

                while True:
                    line = md.readline()

                    if not line and not items['elems']:
                        break

                    if (line.strip() == '' or not line) and items['elems']:
                        print('multiline items: ', items)
                        converted = convert_multiline(items)
                        items['type'] = None
                        items['elems'] = []
                    elif line.strip() == '':
                        continue
                    else:
                        converted = parse_line(line)

                    if isinstance(converted, dict):
                        items['type'] = converted['type']
                        items['elems'].append(converted['item'])
                        continue
                    html.write(converted)
            pass
    except FileNotFoundError:
        exit(f'Missing {md_file}')


def parse_line(line):
    """Search a line for markdown syntax"""
    identifiers = ('#', '-', '*')

    if line[0] not in identifiers:
        line = extract_multiline_items(line, None, 'p')
    if '# ' in line:
        line = convert_headings(line)
    if '- ' in line:
        line = extract_multiline_items(line, '- *', 'ul')
    if '* ' in line:
        line = extract_multiline_items(line, r'\* *', 'ol')
    return line


def convert_multiline(items):
    """Create html for multiline items"""
    type = items['type']
    elems = items['elems']

    print('elems: ', elems)

    line = f'<{type}>\n'

    if type != 'p':
        for elem in elems:
            line += f'\t<li>{elem}</li>\n'
        line += f'</{type}>\n'
    else:
        line = '<p>'
        for i in range(len(elems)):
            br = ''
            if len(elems) > 1 and i < len(elems) - 1:
                br = ' <br /> '
            line += elems[i] + br
        line += '</p>\n'
    return line


def convert_headings(line):
    """Convert markdown headings to html"""
    heading_level = line.count('#')
    line = re.sub('(#+) +', f'<h{heading_level}>', line)
    line = line.replace('\n', f'</h{heading_level}>\n')
    return line


def extract_multiline_items(line, type, tag):
    """Extract multiline items: unordered lists, ordered lists"""
    if type is not None:
        line = re.sub(type, '', line)
    line = line.replace('\n', '')
    return {
        'type': tag,
        'item': line
    }


def extract_ordered_lists(line):
    """Extract ordered list items"""


if __name__ == '__main__':
    main()
