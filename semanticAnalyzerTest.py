from syntaxTree import build_trees, TokenNode

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(message)

class SemanticAnalyzer:
    def __init__(self, root: TokenNode, previous_root: TokenNode = None):
        self.root = root
        self.previous_root = previous_root

    def analyze(self):
        self.verify_acotations(self.root)
        self.verify_dialogue_characters(self.root. self.previous_root)

    def verify_dialogue_characters(self, node: TokenNode, previous_node: TokenNode = None):
        # Verify that dialogues have a character in the previous line
        if node.token_type == 'DIALOGO':
            if not previous_node or previous_node.token_type != 'PERSONAJE':
                raise SemanticError(f"Dialogue in line {node.line_number} and position {node.line_position} must have a character in the previous line.")

    def verify_acotations(self, node: TokenNode):
        if node.token_type == 'ACOTACION':
            parent_type = node.parent.token_type if node.parent else None
            if parent_type not in ['DIALOGO', 'ACCION']:
                raise SemanticError(f"Acotation in line {node.line_number} and position {node.line_position} must be within a dialogue or an action.")
        
        for child in node.children:
            self.verify_acotations(child)

    def verify_scenes_with_transitions(self, node: TokenNode):
        pass


def run_semantic_analyzer(root_nodes):
    # Create an instance of the semantic analyzer and execute it for every root node
    previous_root = None
    first_scene = False
    for root in root_nodes:
        #if root 
        semantic_analyzer = SemanticAnalyzer(root, previous_root)
        previous_root = root
        try:
            semantic_analyzer.analyze()
            print(f"Semantic analysis passed for {root.token_id}.")
        except SemanticError as e:
            print(f"Semantic analysis failed for {root.token_id}: {e}")

    return True