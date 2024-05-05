from Production import *

def scan(token):
    if token == 'ws':
        try:
            return WHITESPACE
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == 'characters':
        try:
            return CHARACTERS
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '/*':
        try:
            return LEFTCOMMENT
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '*/':
        try:
            return RIGHTCOMMENT
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '%token':
        try:
            return TOKEN
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '|':
        try:
            return OR
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == 'IGNORE':
        try:
            return IGNORE
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == 'minusword':
        try:
            return WORDMIN
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == 'mayusword':
        try:
            return WORDMAY
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '%%':
        try:
            return SPLIT
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == ':':
        try:
            return TWOPOINTS
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == ';':
        try:
            return FINISHDECLARATION
        except NameError:
            return f'Token indefinido: {{token}}'
    return f'Token indefinido: {{token}}'

def output_scanner(simulation):
    with open('./definition/output_definitions.txt', 'w') as f:
        for s in simulation:
            scanner = scan(s[0])
            f.write(f'{s} ==> Definicion: {scanner}\n')
