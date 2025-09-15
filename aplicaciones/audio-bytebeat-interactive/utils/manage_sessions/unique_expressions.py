#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from sys import argv


def get_uniques(files):
    result = set()
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            expressions = []
            for item in data:
                expr = item['data']
                if not expr.startswith('--'):
                    expressions.append(expr)
            result.update(expressions)
    return list(result)

if __name__ == '__main__':
    if len(argv) > 1:
        files = argv[1:]
        resp = get_uniques(files)
        print('\n'.join(sorted(resp)))
