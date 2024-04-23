class Simulation:
    def __init__(self, dfa, sfPoint, test):
        self.dfa = dfa
        self.start = sfPoint[0]
        self.end = sfPoint[1]
        self.tokens = sfPoint[2]
        self.test = test
        self.result = []
        
    def simulate(self):
        text = ""
        position = self.start[0]
        for token in self.test:
            for lex in token:
                done = False
                exists = True
                value = ord(lex)
                while not (done):
                    
                    for pos in self.dfa:
                        if pos[0] == position and pos[1] == str(value):
                            text += chr(value)
                            position = pos[2]
                            exists = False
                            done = True
                            break
                
                    if exists:
                        if position == self.start[0]:
                            self.result.append(["lexical error", lex])
                            text = ""
                            done = True
                        else:
                            
                            indice = self.end.index(position)
                            self.result.append([self.tokens[indice].replace("#",""), text])
                            text = ""
                            position = self.start[0]

        if text:
            if position == self.start[0]:
                self.result.append(["lexical error", text])
                text = ""
            else:
                indice = self.end.index(position)
                self.result.append([self.tokens[indice].replace("#",""), text])
                text = ""
                position = self.start[0]
            
                        
        return self.result