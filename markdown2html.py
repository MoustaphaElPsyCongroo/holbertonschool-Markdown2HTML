#!/usr/bin/python3
"""Markdown to html parser"""
from sys import argv, exit

argslen = len(argv) - 1


def main():
    if argslen < 2:
        exit('Usage: ./markdown2html.py README.md README.html')

    md_file = argv[1]
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            pass
    except FileNotFoundError:
        exit(f'Missing {md_file}')


if __name__ == '__main__':
    main()
