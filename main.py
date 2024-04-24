import time
from shuntingyard import Postfix
from readyalex import Yalex
from arbol import SyntacticTree
from dfa_directly import DFA
from Def import Definition
from Simulate import Simulation
from readyalp import Yalp

test_yalex = "./yalex/slr-1.yal"


print("\n===========================================================================================")
print("\nBienvenido al Laboratorio E de Compiladores\n")
print("===========================================================================================\n")

with open(test_yalp) as f:
    testLines = f.readlines()

start_time = time.time()

regex, token_functions = Yalex(yalex).read_yalex()


post = Postfix(regex)
postfix = post.shunting_yard()
print("\npostfix: {postfix}\n")


tree = SyntacticTree(yalex)
tree.tree_construction(postfix)
tree.visualize_tree()

result = tree.left_most()

time.sleep(1)
end_time = time.time()

total_time = end_time - start_time

print("\n===========================================================================================")

print(f"\nLa construccion del arbol sintactico tuvo un tiempo de ejecucion de {total_time} segundos\n")

print("===========================================================================================\n")


# Parte del laboratorio D

dfa = DFA(result)
direct= dfa.Dstate()

dfa.visualize_dfa(direct[0], direct[1], 'yalp_analyzer.yal')


print(f"\ntoken_functions: {token_functions}\n")
    
simulation = Simulation(direct[0], direct[1], testLines)
sim = simulation.simulate()

python_file = Definition(token_functions)
python_file.create_python()
python_file.create_scanner_output()

print(f"\nsimulacion: {sim}\n")


from scann import *

output_scanner(sim)

yalp = Yalp(test_yalex, sim)
yalp.init_construction()
yalp.subset_construction()
yalp.show_graph('slr-1.yalp')

parse = Parser(yalp.transitions, yalp.subsets, yalp.subsets_num, yalp.subproductions)
parse.construct_table()
parse.draw_table()