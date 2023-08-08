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
                while True:
                    line = md.readline()

                    if not line:
                        break
                    converted = convert_line(line)
                    html.write(converted)

            pass
    except FileNotFoundError:
        exit(f'Missing {md_file}')


def convert_line(line):
    """Converts a markdown line to an html one"""
    if '#' in line:
        heading_level = line.count('#')
        line = re.sub('(#+) +', f'<h{heading_level}>', line)
        line = line.replace('\n', f'</h{heading_level}>\n')
    return line


if __name__ == '__main__':
    main()
