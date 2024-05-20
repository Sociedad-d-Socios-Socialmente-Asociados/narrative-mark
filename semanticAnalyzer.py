from typing import Any, Generator, List
from syntaxTree import build_trees, TokenNode

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(message)

class SemanticAnalyzer:
    def __init__(self, root_nodes: List[TokenNode], token_list: Generator[tuple[str, str | None, str, str | Any | None, Any, int] | Any, Any, None]):
        self.root_nodes = root_nodes
        self.token_list = list(token_list)

    def analyze(self):
        self.verify_title()
        self.verify_single_title()
        self.verify_no_single_acotations()
        self.verify_no_multiple_tokens_per_line()
        self.verify_dialogue_preceded_by_character()
        self.verify_scenes()

    def verify_title(self):
        if self.root_nodes[0].token_type != 'TITULO':
            raise SemanticError(f"Title must be the first element in the script.")
        
    def verify_single_title(self):
        title_count = sum(1 for token in self.token_list if token[1] == 'TITULO')
        if title_count != 1:
            raise SemanticError(f"Script must contain exactly one title. Found {title_count} titles.")
        
    def verify_scenes(self):
        last_token_type = None
        for token in self.token_list:
            token_type = token[1]
            if token_type == 'ESCENA':
                if last_token_type is not None and last_token_type != 'TRANSICION' and last_token_type != 'TITULO':
                    raise SemanticError(f"Scene '{token[2]}' at line {token[4]} must be preceded by a transition or be the first scene.")
            last_token_type = token_type

    def verify_no_single_acotations(self):
        for root in self.root_nodes:
            if root.token_type == 'ACOTACION':
                raise SemanticError(f"Acotations must be within a dialogue or an action (line {root.line_number}).")

    def verify_no_multiple_tokens_per_line(self):
        line_tokens = {}
        for root in self.root_nodes:
            if root.line_number not in line_tokens:
                line_tokens[root.line_number] = []
            line_tokens[root.line_number].append(root.token_type)

        for line_number, tokens in line_tokens.items():
            if len(tokens) > 1:
                raise SemanticError(f"Multiple tokens found on line {line_number}: {tokens}. Only one token allowed per line unless nested.")
    
    def verify_dialogue_preceded_by_character(self):
        last_token_type = None
        for token in self.token_list:
            token_type = token[1]
            if token_type == 'DIALOGO':
                if last_token_type != 'PERSONAJE':
                    raise SemanticError(f"Dialogue '{token[2]}' at line {token[4]} must be preceded by a character name.")
            last_token_type = token_type

    def verify_no_multiple_transitions(self):
        last_token_type = None
        for token in self.token_list:
            token_type = token[1]
            if token_type == 'TRANSICION':
                if last_token_type == 'TRANSICION':
                    raise SemanticError(f"You cannot have multiple transitions in a row. Found two transitions at line {token[4]}.")
            last_token_type = token_type
    
def run_semantic_analyzer(root_nodes, token_list):
    # Create an instance of the semantic analyzer
    semantic_analyzer = SemanticAnalyzer(root_nodes, token_list)
    try:
        semantic_analyzer.analyze()
        print(f"Semantic analysis passed.")
        return True
    except SemanticError as e:
        print(f"Semantic analysis failed: {e}")
        return False

    