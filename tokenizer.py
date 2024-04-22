import re

def tokenize(code):
    keywords = ['if', 'else', 'while', 'for', 'return', 'print']
    token_specification = [
        ('TRANSICIÓN', r'>>.*\n'),
        ('ESCENA', r'>.*\n'),
        ('ACCIÓN', r'<[^>]+>'),
        ('PERSONAJE', r'@\w+\b'),
        ('ACOTACIÓN', r'\([^)]+\)'),
        ('DIÁLOGO', r'--.*\n'),
        ('TÍTULO', r'\[T:\s*[^\]]+\]'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        elif kind in ('ACCIÓN', 'ACOTACIÓN'):
            metatext = value[1:-1]
        elif kind == 'PERSONAJE':
            metatext = value[1:]
        elif kind in ('DIÁLOGO', "TRANSICIÓN"):
            metatext = value[2:-1]
        elif kind == 'TÍTULO':
            metatext = re.search(r'\[T:\s*(.*?)\]', value).group(1)
        else:
            metatext = None

        yield (kind, value, metatext, line_num, mo.start()-line_start)

code = '''
    [T: La pelea]
    [T:La pelea sin espacio]
    >1. int. piso compartido / recibidor y comedor - tarde
    @Francisco le dice a @Fernando --Eres un bobo mi pana
    --Creo jaja
    <@Francisco procede a pegarle a @Fernando> (riéndose)
    >> Fundido a negro
    >>Fundido disco gay jaja
    <Nadie responde. @Rubén deja el cucharón (mientras ve fijamente a @Mario) y se dirige al pasillo.>
'''

print('FIRST LEVEL TOKENS:')
tokenized_code = tokenize(code)
to_metatokenize = ""
for token in tokenized_code:
    print(token)
    if token[2] is not None:
        to_metatokenize += token[2] + "\n"

# TODO: Poner bien las ubicaciones de los metatokens, salen las ubicaciones del nuevo string
print('\nSECOND LEVEL TOKENS:')
metatokenized_code = tokenize(to_metatokenize)
to_metametatokenize = ""
for token in metatokenized_code:
    print(token)
    if token[2] is not None:
        to_metametatokenize += token[2] + "\n"

# TODO: Poner bien las ubicaciones de los metametatokens, salen las ubicaciones del nuevo string
print('\nTHIRD LEVEL TOKENS:')
metametatokenized_code = tokenize(to_metametatokenize)
for token in metametatokenized_code:
    print(token)
