"""
Algoritmo de Thompson
Algortimo que convierte una expresión regular a un autómata finito no determinista
"""
import pydotplus

def create_dfn_graph(states, acceptance_states, transitions, symbols, start_state):
    # Convert sets to strings
    states = [str(state) for state in states]
    start_state = str(start_state)
    acceptance_states = [str(state) for state in acceptance_states]

    # Create a DOT format representation of the DFA
    dot = pydotplus.Dot()
    dot.set_rankdir("LR")  # Use 'TB' for top to bottom layout
    dot.set_prog("neato")

    # Create nodes for each state
    state_nodes = {}
    for state in states:
        node = pydotplus.Node(state)
        if state == start_state:
            node.set_name("Start")
            node.set_shape("circle")
            node.set_style("filled")

        if state in acceptance_states:
            node.set_shape("doublecircle")  # Final states are double circled
        node.set_fontsize(12)  # Set font size
        node.set_width(0.6)  # Set the desired width
        node.set_height(0.6)  # Set the desired height
        state_nodes[state] = node
        dot.add_node(node)

    # Add transitions as edges
    for (source, symbol, target) in transitions:
        edge = pydotplus.Edge(state_nodes[str(source)], state_nodes[str(target)], label=symbol)
        dot.add_edge(edge)

    return dot

def operando(element, estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo):
    if element != '𝜀':
        if element in alfabeto:
            alfabeto.remove(element)
            alfabeto.append(element)
        else:
            alfabeto.append(element)
        
    transiciones.append((contadorEstados, element, contadorEstados + 1))
    stack_grupos.append([element, contadorEstados, contadorEstados + 1])
    contador_grupo += 1
    estados.append(contadorEstados)
    contadorEstados += 1
    estados.append(contadorEstados)
    contadorEstados += 1
    
    return estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo

def operador_or(element, estados, transiciones, stack_grupos, contadorEstados, contador_grupo):
    grupo2 = stack_grupos.pop()
    grupo1 = stack_grupos.pop()
    contador_grupo -= 2
    estado_inicial = grupo1[1]
    estado_final = 0

    transiciones_temp = transiciones.copy()
    for tran in transiciones:
        if tran[0] == grupo1[1]:
            index = transiciones.index(tran)
            transiciones_temp.insert(index, (tran[0], '𝜀', tran[2]))
            index += 1
            flag = False
            while index < len(transiciones_temp):
                transi = transiciones_temp[index]
                if  transi[2] == grupo1[2] and flag == False:
                    flag = True
                    transiciones_temp[index] = (transi[0] + 1, transi[1], transi[2] + 1)
                    index += 1
                    transiciones_temp.insert(index, (transi[2] + 1, '𝜀', grupo2[2] + 2))
                    estados.append(contadorEstados)
                    contadorEstados += 1
                    estados.append(contadorEstados)
                    contadorEstados += 1
                    index += 1
                    continue
                transiciones_temp[index] = (transi[0] + 1, transi[1], transi[2] + 1)
                index += 1
            break
    transiciones = transiciones_temp
    grupo1 = [grupo1[0], grupo1[1], grupo2[2]+3]

    transiciones_temp = transiciones.copy()
    for tran in transiciones:
        if tran[0] == grupo2[1]+1 and tran[2] != grupo1[2]:
            index = transiciones.index(tran)
            transiciones_temp.insert(index, (grupo1[1], '𝜀', tran[0]))
            index += 1
            transiciones_temp.append((grupo2[2]+1, '𝜀', grupo2[2] + 2))
            estado_final = grupo2[2] + 2
            break
    transiciones = transiciones_temp
    grupo2 = [grupo2[0], estado_inicial, estado_final]

    stack_grupos.append([element, grupo1[1], grupo2[2]])
    contador_grupo += 1
    return estados, transiciones, stack_grupos, contadorEstados, contador_grupo

def operador_concat(element, estados, transiciones, stack_grupos, contadorEstados, contador_grupo):
    grupo2 = stack_grupos.pop()
    grupo1 = stack_grupos.pop()
    contador_grupo -= 1
    estado_inicial = grupo1[1]
    estado_final = grupo2[2]-1

    transiciones_temp = transiciones.copy()
    for tran in transiciones:
        if tran[2] == grupo1[2] and tran[0] == grupo1[2]-1:
            index = transiciones.index(tran)
            index += 1
            while index < len(transiciones_temp):
                transi = transiciones_temp[index]
                transiciones_temp[index] = (transi[0] - 1, transi[1], transi[2] - 1)
                index += 1
            estados.pop()
            contadorEstados -= 1
            break
    transiciones = transiciones_temp
    stack_grupos.append([element, estado_inicial, estado_final])
    return estados, transiciones, stack_grupos, contadorEstados, contador_grupo

def operador_kleene(element, estados, transiciones, stack_grupos, contadorEstados, contador_grupo):
    grupoAnterior = stack_grupos.pop()
    estado_inicial = grupoAnterior[1]
    estado_final = 0

    transiciones_temp = transiciones.copy()
    for tran in transiciones:
        if tran[0] == grupoAnterior[1]:
            index = transiciones.index(tran)
            transiciones_temp[index] = (tran[0] + 1, tran[1], tran[2] + 1)
            transiciones_temp.insert(index, (tran[0], '𝜀', tran[2]))
            index += 2
            while index < len(transiciones_temp):
                transi = transiciones_temp[index]
                transiciones_temp[index] = (transi[0] + 1, transi[1], transi[2] + 1)
                index += 1
            estados.append(contadorEstados)
            contadorEstados += 1
            estados.append(contadorEstados)
            contadorEstados += 1
            transiciones_temp.append((grupoAnterior[2] + 1, '𝜀', grupoAnterior[1] + 1))
            transiciones_temp.append((grupoAnterior[1] + 1, '𝜀', grupoAnterior[2] + 1))
            estado_final = contadorEstados - 1
            transiciones_temp.append((contadorEstados - 2, '𝜀', contadorEstados - 1))
            break
    stack_grupos.append([element, estado_inicial, estado_final])
    transiciones = transiciones_temp
    return estados, transiciones, stack_grupos, contadorEstados, contador_grupo

def operador_plus(element, estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo):
    grupoAnterior = stack_grupos[-1]
    estado_inicial = grupoAnterior[1]

    estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo = operando(grupoAnterior[0], estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo)

    estados, transiciones, stack_grupos, contadorEstados, contador_grupo = operador_kleene('*', estados, transiciones, stack_grupos, contadorEstados, contador_grupo)

    estados, transiciones, stack_grupos, contadorEstados, contador_grupo = operador_concat(element, estados, transiciones, stack_grupos, contadorEstados, contador_grupo)
    
    grupo = stack_grupos.pop()
    stack_grupos.append([element, estado_inicial, grupo[2]])

    return estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo

def operador_optional(element, estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo):
    grupoAnterior = stack_grupos[-1]
    estado_inicial = grupoAnterior[1]

    estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo = operando('𝜀', estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo)

    estados, transiciones, stack_grupos, contadorEstados, contador_grupo = operador_or('|', estados, transiciones, stack_grupos, contadorEstados, contador_grupo)
    
    grupo = stack_grupos.pop()
    stack_grupos.append([element, estado_inicial, grupo[2]])

    return estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo


''' Función que ejecuta el algoritmo de Thompson '''
def exec(expr, output_text_file):
    # Variable para almacenar la cantidad total de estados que se van a crear
    contadorEstados = 0

    # Vamos guardando los estados en una lista
    estados = []
    # Vamos guardando los símbolos del alfabeto en una lista
    alfabeto = []
    # Vamos guardando las transiciones en una lista de tuplas
    transiciones = []
    # Vamos guardando los estados de aceptación en una lista
    estado_inicial = 0
    # Vamos guardando los estados de aceptación en una lista
    estados_aceptacion = []

    # Partimos la expresión regular en una lista de caracteres
    stri = list(expr)

    " Algoritmo de Thompson (Creamos el autómata finito no determinista) "

    # Declaramos un contador para recorrer la lista de grupos
    linea = 0
    stack_grupos = []
    contador_grupo = 0
    while linea < len(stri):
        element = stri[linea]
        if element == '.':
            estados, transiciones, stack_grupos, contadorEstados, contador_grupo = operador_concat(element, estados, transiciones, stack_grupos, contadorEstados, contador_grupo)

        elif element == '|':
            estados, transiciones, stack_grupos, contadorEstados, contador_grupo = operador_or(element, estados, transiciones, stack_grupos, contadorEstados, contador_grupo)

        elif element == '*':
            estados, transiciones, stack_grupos, contadorEstados, contador_grupo = operador_kleene(element, estados, transiciones, stack_grupos, contadorEstados, contador_grupo)

        elif element == '+':
            estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo = operador_plus(element, estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo)
            
        elif element == '?':
            estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo = operador_optional(element, estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo)
            
        else:
            estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo = operando(element, estados, transiciones, stack_grupos, alfabeto, contadorEstados, contador_grupo)

        linea += 1

    estados_aceptacion.append(estados[-1])

    alfabeto = [s for s in alfabeto if s != '.']

    with open(output_text_file, 'w', encoding='utf-8') as file:
        file.write(f"ESTADOS = {{{', '.join(map(str, estados))}}}\n")
        file.write(f"SIMBOLOS = {{{', '.join(alfabeto)}}}\n")
        file.write(f"INICIO = {{{estado_inicial}}}\n")
        file.write(f"ACEPTACION = {{{', '.join(map(str, estados_aceptacion))}}}\n")
        transiciones_str = ', '.join([f"({t[0]}, {t[1]}, {t[2]})" for t in transiciones])
        file.write(f"TRANSICIONES = {{{transiciones_str}}}\n")

    pydotplus.find_graphviz()

    graph = create_dfn_graph(estados, estados_aceptacion, transiciones, alfabeto, estado_inicial)

    # Save or display the graph
    png_file_path = "pngs/dfn_graph.png"
    graph.write_png(png_file_path)  # Save PNG file

    return estados, alfabeto, transiciones, estado_inicial, estados_aceptacion