import copy
import graphviz
import networkx as nx
from readyalex import *


class Yalp(object):
    def __init__(self, file, simulation):
        self.number = 0
        self.subtoken = []
        self.tokens = []
        self.simulation = simulation
        self.productions = [] 
        self.subproductions = []
        self.subsets= [] 
        self.subsets_num = [] 
        self.ocurrence = [] 
        self.transitions = [] 

        reader = Yalex(file)
        _,token_functions = reader.read_yalex()

        for sublist in token_functions:
            if 'return' in sublist[1]:
                sublist[1] = sublist[1].replace('return ', '')
        self.tokenFunctions = token_functions
        
        
    def init_construction(self):
        is_comment = False
        is_token = False
        is_expression = True
        function_name = ""
        production_tokens = []
        has_separator = False

        for token_type, *values in self.simulation:
            if token_type == "/*":
                is_comment = True

            if not is_comment:
                if token_type == "%%":
                    has_separator = True

                if has_separator:
                    if is_expression and token_type == "minusword":
                        function_name = values[0][0].upper()
                        is_expression = False
                    elif not is_expression:
                        if token_type == "minusword":
                            production_tokens.append(values[0][0].upper())
                        elif token_type == "mayusword":
                            production_tokens.append(values[0])
                        elif token_type == "|":
                            self.productions.append([function_name, production_tokens])
                            production_tokens = []
                        elif token_type == ";":
                            if production_tokens:
                                self.productions.append([function_name, production_tokens])
                                production_tokens = []
                            is_expression = True

                else:
                    if token_type == "%token":
                        is_token = True
                    elif token_type == "IGNORE":
                        is_token = False

                    if is_token and token_type == "mayusword":
                        self.tokens.append(values[0])
                        self.subtoken.append(values[0])
                    elif not is_token and token_type == "mayusword":
                        self.tokens.remove(values[0])
                        self.subtoken.remove(values[0])

            if token_type == "*/":
                is_comment = False

        self.tokens = [token_func[0] if token == token_func[1] else token for token in self.tokens for token_func in self.tokenFunctions]

        for production in self.productions:
            for i, token in enumerate(production[1]):
                for subtoken in self.subtoken:
                    if token == subtoken:
                        index = self.subtoken.index(subtoken)
                        production[1][i] = self.tokens[index]

        
    def subset_construction(self):

        initial_value = self.productions[0][0]
        self.productions.insert(0, [initial_value + "'", [initial_value]])
        self.subproductions = copy.deepcopy(self.productions)

        for production in self.productions:
            production[1].insert(0, ".")

        self.closure([self.productions[0]])

        while self.ocurrence:
            self.goto(self.ocurrence.pop(0))

        initial_state = self.productions[0][0]
        for subset in self.subsets:
            for item in subset:
                accept_index = item[1].index(".")
                if accept_index - 1 >= 0:
                    if item[0] == initial_state and item[1][accept_index - 1] == initial_state[:-1]:
                        final_index = self.subsets.index(subset)
                        self.transitions.append([self.subsets_num[final_index], "$", "accept"])


        
    def closure(self, item, elem=None, cycle=None):
        closure_array = item.copy()

        while True:
            prev_length = len(closure_array)
            for item in closure_array:
                dot_index = item[1].index(".")
                if dot_index + 1 < len(item[1]):
                    next_val = item[1][dot_index + 1]
                    new_items = [y for y in self.productions if y[0] == next_val and y not in closure_array]
                    closure_array.extend(new_items)

            if prev_length == len(closure_array):
                break

        sorted_items = sorted(closure_array, key=lambda x: x[0])

        if sorted_items not in self.subsets:
            self.subsets.append(sorted_items)
            self.subsets_num.append(self.number)
            self.number += 1
            self.ocurrence.append(sorted_items)

        if elem is not None and cycle is not None:
            start_index = self.subsets.index(cycle)
            end_index = self.subsets.index(sorted_items)
            self.transitions.append([self.subsets_num[start_index], elem, self.subsets_num[end_index]])

        
    def goto(self, ocurrence):
        elements = list(set(x[1][x[1].index(".") + 1] for x in ocurrence if x[1].index(".") + 1 < len(x[1])))

        for elem in elements:
            temporal = [copy.deepcopy(y) for y in ocurrence if y[1].index(".") + 1 < len(y[1]) and y[1][y[1].index(".") + 1] == elem]

            for item in temporal:
                dot_index = item[1].index(".")
                if dot_index + 1 < len(item[1]):
                    item[1][dot_index], item[1][dot_index + 1] = item[1][dot_index + 1], item[1][dot_index]

            self.closure(temporal, elem, ocurrence)


    def render_graph(self, G, name):
        
        description = (f"LR(0) of {name}")
        dot = graphviz.Digraph(comment=description)
        
        dot.attr(
            labelloc="t",
            label=description
        )

        for node, attrs in G.nodes(data=True):
            dot.node(str(node), label=str(attrs['label']).replace("'", "").replace('"', ''), fontsize="10", shape="rectangle")

        for source, target, attrs in G.edges(data=True):  
            dot.edge(str(source), str(target), label=attrs['label'], fontsize="10")

        output_filename = f"LR(0) of {name}" 
        
        dot.render(f"./Yalpspngs/{output_filename}", view=True, format='png')

    
    def show_graph(self, filename):
        
        G = nx.DiGraph()


        for i, arr in enumerate(self.subsets):
            label = f"I{i}\n"
            for item in arr:
                label += str(item) + "\n"
            G.add_node(i, label=label)


        for t in self.transitions:
            from_node, label, to_node = t
            G.add_edge(from_node, to_node, label=label)
            

        for node in G.nodes():
            if 'label' not in G.nodes[node]:
                G.nodes[node]['label'] = str(node)
                
        self.render_graph(G, filename)
    
    