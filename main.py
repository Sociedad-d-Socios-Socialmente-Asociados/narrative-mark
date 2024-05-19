from syntaxTree import run_syntax_tree
from tokenizer import run_tokenizer

doc_path = input("Enter the name or path of the file to compile: ")

token_list = run_tokenizer(doc_path)
errors, success = run_syntax_tree(token_list)

if success:
    print("Syntax tree is valid.")
else:
    print("Syntax tree is invalid.")
    print(errors)

# TODO: Semantic Analysis