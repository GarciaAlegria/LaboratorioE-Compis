import time
from shuntingyard import Postfix
from readyalex import Yalex
from arbol import SyntacticTree
from dfa_directly import DFA
from Def import Definition
from Simulate import Simulation
from readyalp import Yalp
from Parser import Parser

#Laboratorio anterior  
Myyalex = "./yalex/yalp_analyzer.yal"


#Se puede cambiar el archivo de entrada para probar con otro archivo
Myreadyalex = "./yalex/YaLex2.yal"
Myreadyalp = "./yalp/YaPar2.txt"


print("\n===========================================================================================")
print("\nBienvenido al Laboratorio E de Compiladores\n")
print("===========================================================================================\n")

with open(Myreadyalp) as f:
    testLines = f.readlines()

start_time = time.time()

regex, token_functions = Yalex(Myyalex).read_yalex()


post = Postfix(regex)
print("===========================================================================================")
print("regex:")
print("===========================================================================================")
print(regex)
print("===========================================================================================")

postfix = post.shunting_yard()
print("===========================================================================================")
print("postfix:")
print("===========================================================================================")
print(postfix)
print("===========================================================================================")


tree = SyntacticTree(Myyalex)
tree.tree_construction(postfix)
tree.visualize_tree()

result = tree.left_most()

time.sleep(1)
end_time = time.time()

total_time = end_time - start_time

print("===========================================================================================")
print(f"\ntiempo de ejecucion del arbol es de {total_time} segundos")
print("===========================================================================================")


dfa = DFA(result)
direct= dfa.Dstate()

dfa.visualize_dfa(direct[0], direct[1], 'yalp_analyzer.yal')

print("===========================================================================================")
print("tokens y funciones:")
print("===========================================================================================")
print(f"token_functions: {token_functions}\n")
    
simulation = Simulation(direct[0], direct[1], testLines)
sim = simulation.simulate()

python_file = Definition(token_functions)
python_file.create_python()
python_file.create_scanner_output()

print("===========================================================================================")
print("Yalp interpreter:")
print("===========================================================================================")
print(f"Archivo Yalp: {sim}\n")

print("===========================================================================================")
print("simulacion:")
print("===========================================================================================")
print(f"simulacion: {sim}\n")


from scann import *

output_scanner(sim)

yalp = Yalp(Myreadyalex, sim)
yalp.init_construction()
yalp.subset_construction()
yalp.show_graph('YaPar4.yalp')

parse = Parser(yalp.transitions, yalp.subsets, yalp.subsets_num, yalp.subproductions)
parse.construct_table()
parse.draw_table()