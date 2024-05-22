import os
from datetime import timedelta
from time import perf_counter_ns
from pdfGenerator import generate_pdf
from semanticAnalyzer import run_semantic_analyzer
from syntaxTree import run_syntax_tree
from tokenizer import run_tokenizer

# Function to check if the file is a .txt files
def is_txt_file(file_path):
    return os.path.splitext(file_path)[1].lower() == ".txt"


doc_path = input("Enter the name or path of the file to compile: ")

global_start = perf_counter_ns()

# Verify that the file is a .txt file
if not is_txt_file(doc_path):
    print("The file must be a .txt file.")
    exit()

try:
    with open(doc_path, "r", encoding="utf-8") as file:
        code = file.read()
except FileNotFoundError:
    print(
        "File not found. If you entered the name of the file, make sure it is in the same folder as the compiler, otherwise, enter the full path of the file."
    )
    exit()

token_list = run_tokenizer(code=code)

print("Tokenization complete. Running syntax tree...")
root_nodes, success = run_syntax_tree(token_list)

if success:
    print("Syntax tree is valid.")
    if run_semantic_analyzer(root_nodes, token_list):
        print("Compilation successful. Creating PDF...")
        generate_pdf(root_nodes, token_list, "output.pdf")
        print(
            f"Compilation took: {timedelta(seconds=(perf_counter_ns() - global_start) / 1e9)}"
        )
else:
    print("SyntaxError:", root_nodes)
