from semanticAnalyzer import run_semantic_analyzer
from syntaxTree import run_syntax_tree
from tokenizer import run_tokenizer

doc_path = input("Enter the name or path of the file to compile: ")

token_list = run_tokenizer(doc_path)
root_nodes, success = run_syntax_tree(token_list)

if success:
    print("Syntax tree is valid.")
else:
    print("Syntax tree is invalid.")
    print(root_nodes)

# TODO: Semantic Analysis
if run_semantic_analyzer(root_nodes, token_list):
    print("Compiling...") 