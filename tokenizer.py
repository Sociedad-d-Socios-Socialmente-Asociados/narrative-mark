import re

def tokenize(code):
    token_specification = [
        ('TRANSICIÓN', r'>>.*'),
        ('ESCENA', r'>.*'),
        ('ACCIÓN', r'<[^>]+>'),
        ('PERSONAJE', r'@(?:[^\s@]+(?:@[^\s@]+)*)'),
        ('ACOTACIÓN', r'\([^)]+\)'),
        ('DIÁLOGO', r'--.*'),
        ('TÍTULO', r'\[T:\s*[^\]]+\]'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    # Function to recursively find nested tokens
    def find_tokens(text, line_num, line_start_pos=0):
        for mo in re.finditer(tok_regex, text, re.UNICODE):
            kind = mo.lastgroup
            value = mo.group()
            start_pos = mo.start()

            # Update line_num based on the number of newlines before the token
            line_num += value.count('\n')

            if kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            elif kind in ('ACCIÓN', 'ACOTACIÓN'):
                metatext = value[1:-1]
            elif kind == 'PERSONAJE':
                metatext = value[1:]
            elif kind in ('DIÁLOGO', 'TRANSICIÓN'):
                metatext = value[2:]
            elif kind == 'TÍTULO':
                metatext = re.search(r'\[T:\s*(.*?)\]', value).group(1)
            elif kind == 'ESCENA':
                metatext = value[1:]
            else:
                metatext = None

            token_pos = start_pos + line_start_pos

            yield (kind, value, metatext, line_num, token_pos)

            # If the token is a container token, recursively find tokens inside it
            if kind in ('ACCIÓN', 'ACOTACIÓN', 'DIÁLOGO', 'ESCENA'):
                for nested_token in find_tokens(metatext, line_num, token_pos + 1):
                    yield nested_token

        line_num += 1  # Increment line_num for each line

    # Start tokenization
    line_num = 1
    for line in code.split('\n'):
        for token in find_tokens(line, line_num):
            yield token
        line_num += 1

file_name = input("Enter the name of the file: ")

try:
    with open(file_name, 'r', encoding='utf-8') as file:
        code = file.read()
except FileNotFoundError:
    print("File not found.")
    exit()

print('TOKEN LIST:')
tokenized_code = tokenize(code)
for token in tokenized_code:
    print(token)
