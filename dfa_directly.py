'''
Algoritmo de Conversión Directa
'''

import string
import graphviz

class DFA:
    def __init__(self,postfix):
        self.postfix = postfix
        #agregar el # de ultimo para la cadena
        self.postfix.append('#')
        self.postfix.append('•')
        # Nueva lista vacía que se utiliza para ordenar correspondientemente cuando se obtienen los valores
        self.nueva_lista = []

        self.deletable_firstPos = []
        self.deletable_lastPos = []
        self.deletable_nullable = []

        self.newPostfix = []
        self.nullable= []
        self.firstPos= []
        self.lastPos = []
        self.followPos = [] 
        self.q = []
        self.enumerate_states()
        self.construction()
        self.followpos()
    
    # Se enumeran los estados correspondientes
    def enumerate_states(self):
        self.q = list(range(1, 1000))
        self.newPostfix = [self.q.pop(0) if x not in '*|•?+ε' else x for x in self.postfix]


    #se comenzara a armar lo necesario para obtner los conjuntos y asi en los que eston van a viajar
    def construction(self):
        for node in self.newPostfix:
            if str(node) in '*|•?+ε':
                if node == '*':
                    self.nullable.append(True)
                    self.firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    self.deletable_nullable.append(True)
                    self.deletable_firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.deletable_lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    #eliminar uno de cada uno
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)

                elif node == '|':
                    #revisar si es nullable
                    c1 = self.deletable_nullable[len(self.deletable_nullable)-2]
                    c2 = self.deletable_nullable[len(self.deletable_nullable)-1]
                    if c1 == True or c2 == True:
                        self.nullable.append(True)
                        self.deletable_nullable.append(True)
                    else:
                        self.nullable.append(False)
                        self.deletable_nullable.append(False)
                    #eliminar las dos primeras del nullable 
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)

                    #agregar el firstpos
                    first = []
                    first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-2])
                    first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    first.sort()
                    self.firstPos.append(first)
                    self.deletable_firstPos.append(first)
                    #eliminar las dos primeras firstpos
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)

                    #agregar el lastpos
                    last = []
                    last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-2])
                    last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                    last.sort()
                    self.lastPos.append(last)
                    self.deletable_lastPos.append(last)
                    #eliminar las primeras dos lastpos
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                elif node == '•':
                    #revisar si es nullable
                    c1 = self.deletable_nullable[len(self.deletable_nullable)-2]
                    c2 = self.deletable_nullable[len(self.deletable_nullable)-1]
                    if c1 == True and c2 == True:
                        self.nullable.append(True)
                        self.deletable_nullable.append(True)
                    else:
                        self.nullable.append(False)
                        self.deletable_nullable.append(False)
                    #eliminar los dos c1 y c2
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    
                    #agregar el firstpos
                    if c1 == True:
                        first = []
                        first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-2])
                        first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                        first.sort()
                        self.firstPos.append(first)
                        self.deletable_firstPos.append(first)
                        #eliminar las dos primeras first
                        self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                        self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    else:
                        first = []
                        first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-2])
                        self.firstPos.append(first)
                        self.deletable_firstPos.append(first)
                        #eliminar las dos primeras first
                        self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                        self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    #agregar el lastpos
                    if c2 == True:
                        last = []
                        last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-2])
                        last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                        last.sort()
                        self.lastPos.append(last)
                        self.deletable_lastPos.append(last)
                        #eliminar las dos primeras last
                        self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                        self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                    else:
                        last = []
                        last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                        self.lastPos.append(last)
                        self.deletable_lastPos.append(last)
                        #eliminar las dos primeras last
                        self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                        self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                elif node == '?':
                    self.nullable.append(True)
                    self.firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    self.deletable_nullable.append(True)
                    self.deletable_firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.deletable_lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    #eliminar cada uno
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                elif node == '+':
                    #revisar si es nullabel
                    c1 = self.deletable_nullable[len(self.deletable_nullable)-1]
                    # print(c1)
                    if c1 == True:
                        self.nullable.append(True)
                        self.deletable_nullable.append(True)
                    else:
                        self.nullable.append(False)
                        self.deletable_nullable.append(False)
                    #eliminar el del nullabel
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)

                    #insertar el firstpos y lastpos
                    self.firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    self.deletable_firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.deletable_lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    #eliminar uno de fist y las
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)

                elif node == 'ε':
                    self.nullable.append(True)
                    self.firstPos.append([])
                    self.lastPos.append([])

                    self.deletable_nullable.append(True)
                    self.deletable_firstPos.append([])
                    self.deletable_lastPos.append([])
            else:
                self.nullable.append(False)
                self.firstPos.append([node])
                self.lastPos.append([node])

                self.deletable_nullable.append(False)
                self.deletable_firstPos.append([node])
                self.deletable_lastPos.append([node])

        
    def followpos(self):
        #limpiar los deletable
        self.deletable_firstPos = []
        self.deletable_lastPos = []

        #guardar todos los valores para el followpost
        for val in range(len(self.newPostfix)):
            if str(self.newPostfix[val]) not in "*?•+|":
                self.followPos.append([self.newPostfix[val]])
        
        for val in range(len(self.newPostfix)):    
            isnodes = []
            addnodes = []
            
            if self.newPostfix[val] == "*":
                isnodes.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                addnodes.extend(self.deletable_firstPos[len(self.deletable_firstPos)-1])

                
                for nod in range(len(self.followPos)):
                    if self.followPos[nod][0] in isnodes:
                        if len(self.followPos[nod]) > 1:
                            for x in addnodes:
                                if x not in self.followPos[nod][1]:
                                    self.followPos[nod][1].append(x)
                            self.followPos[nod][1].sort()
                        else:
                            self.followPos[nod].append(addnodes)

                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                            
            elif self.newPostfix[val] == "+":
                isnodes.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                addnodes.extend(self.deletable_firstPos[len(self.deletable_firstPos)-1])

                
                for nod in range(len(self.followPos)):
                    if self.followPos[nod][0] in isnodes:
                        if len(self.followPos[nod]) > 1:
                            for x in addnodes:
                                if x not in self.followPos[nod][1]:
                                    self.followPos[nod][1].append(x)
                            self.followPos[nod][1].sort()
                        else:
                            self.followPos[nod].append(addnodes)
                            
                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
            
            elif self.newPostfix[val] == "•":
                c1 = self.deletable_lastPos[len(self.deletable_lastPos)-2]
                c2 = self.deletable_firstPos[len(self.deletable_firstPos)-1]
                isnodes.extend(c1)
                addnodes.extend(c2)

                
                for nod in range(len(self.followPos)):
                    if self.followPos[nod][0] in isnodes:
                        if len(self.followPos[nod]) > 1:
                            for x in addnodes:
                                if x not in self.followPos[nod][1]:
                                    self.followPos[nod][1].append(x)
                            self.followPos[nod][1].sort()
                        else:
                            self.followPos[nod].append(addnodes)

                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)


            elif self.newPostfix[val] == '|':
                
                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                
            elif self.newPostfix[val] == '?':
                
                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
            elif "#" in str(self.newPostfix[val]):
                print(self.newPostfix[val])
            else:
                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

            
        #agregar el ultimo un signo ∅ ya que es el #              
        self.followPos[len(self.followPos)-1].append(["∅"])
         
        #revisar de cada uno de los followpos construidos y revisar si entre ellos tiene #
        for lar in range(len(self.followPos)):
            for value in range(len(self.newPostfix)):
                if self.followPos[lar][0] == self.newPostfix[value]:
                    if "#" in self.postfix[value]:
                        self.followPos[lar][1] = ["∅"]

        
    def Dstate(self):

        sNode = self.firstPos[len(self.firstPos)-1]
        
        final = []
        for x in self.followPos:
            if "∅" in x[1]:
                final.append(x[0])

        #aqui tendra todos los nodos de los cuales viajara
        P0 = []
        P0.append(sNode)
        #obtener las variables que utiliza
        self.variables = []
        for x in self.postfix:
            if x not in "|•*+?":
                if "#" not in x:
                    if x not in self.variables:

                        self.variables.append(x)
        
        tabla = []
        for x in P0:                

            conjuntos = []
            conjuntos.append(x)
            for alfa in self.variables:  
                movement = []
                movement.append(alfa)
                con = []
                for y in x: 

                    for l in range(len(self.postfix)):
                        if self.newPostfix[l] == y and self.postfix[l] == alfa:
                            # print("aceptado: ",self.newPostfix[l])
                            for w in self.followPos:
                                if w[0] == y:
                                    for z in w[1]:
                                        if z not in con:
                                            con.append(z)
                con.sort()

                if con not in P0 and len(con) != 0:
                    P0.append(con)
                if len(con) != 0:
                    movement.append(con)
                    conjuntos.append(movement)

                if conjuntos not in tabla:
                    tabla.append(conjuntos)

        for sub_array in tabla:
            if len(sub_array) > 1:
                for i in range(1,len(sub_array)):

                    new_element = [sub_array[0], sub_array[i][0], sub_array[i][1]]
                    self.nueva_lista.append(new_element)
            else:
                self.nueva_lista.append(sub_array)

        
        #convertir la nueva lista en A,B,C ...
        q = list(string.ascii_uppercase)

        node = []
        alfanode = []
        for x in self.nueva_lista:
            if x[0] not in node:
                node.append(x[0])
                alfanode.append(q.pop(0))

        
        for x in self.nueva_lista:

            if len(x) > 1:
                for y in range(len(node)):

                    if x[0] == node[y]:
                        x[0] = alfanode[y]
                    if x[2] == node[y]:
                        x[2] = alfanode[y]
            else:
                for y in range(len(node)):

                    if x[0] == node[y]:
                        x[0] = "vacio"
        
        self.nueva_lista = [sublista for sublista in self.nueva_lista if 'vacio' not in sublista]
        
        
        start = []
        end = []
        endHash = []

        for ele in range(len(node)):
            if node[ele] == sNode:
                start.extend(alfanode[ele])
            for f in final:
                if f in node[ele]:
                    end.extend(alfanode[ele])
                    for val in range(len(self.newPostfix)):
                        if f == self.newPostfix[val]:
                            endHash.append(self.postfix[val])

        if len(node) == 1:
            end.extend(alfanode[0])
        
        sfPoint=[]
        sfPoint.append(start)
        sfPoint.append(end)  
        sfPoint.append(endHash)
            
        
        return [self.nueva_lista, sfPoint]
    
    def visualize_dfa(self, directAFD, sfPoint, filename):

        inicio = sfPoint[0]
        final = sfPoint[1]
        q_list = set()

        for l in directAFD:
            q_list.add(l[0])
            q_list.add(l[2])

        description = (f"DFA of {filename}")
        
        f = graphviz.Digraph(comment=description)
        
        f.attr(
            labelloc="t",
            label=description
        )
        
        inicio_listo = True

        for name in q_list:
            node_attr = {"name": str(name), "label": str(name)}
            if name in final:
                node_attr.update(shape="doublecircle", style="filled")
            elif name in inicio:
                node_attr.update(style="filled")
            f.node(**node_attr)

        f.node("", shape="plaintext")

        for l in directAFD:
            if l[0] in inicio and inicio_listo:
                f.edge("", str(l[0]), label="")
                inicio_listo = False
            if len(l) > 1:
                if type(l[1]) == int:
                    l[1] = chr(l[1])
                f.edge(str(l[0]), str(l[2]), label=str(l[1]))
            else:
                f.node(str(l[0]))

        f.render(f"./DFA/DFA of {filename}", view=True, format='png')
