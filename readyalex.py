class Yalex(object):
    
    def __init__(self, file):
        self.file = file
    
    def read_yalex(self):
        functions = []
        filter_functions = []
        regex = []
        filter_regex = []
        token_regex = []
        token_functions = []
        word = ""

        with open(self.file, 'r') as file:
            lines = file.read()

        activation = False
        
        for l in lines:
            if activation:
                if l == "|":
                    if regex[len(regex)-1] == "|":
                        word += l
                        pass
                    else:
                        if word != "":
                            word=""
                        regex.append(l.strip())
                else:
                    if l not in ["\n",'\t'] : 
                        word += l
                        if "{" in word and "}" in word:
                            word = word.strip()
                            regex.append(word)
                            word = ""
                        if "(*" in word and "*)" in word:
                            word = ""
                    elif l == "\n":
                        if word:
                            if "{" not in word:
                                word = word.strip()
                                if word != "":
                                    regex.append(word)
                        word+=" "
            else:
                word+=l
                
                if '\n' in word:
                    if len(word) > 0:
                        if "let" in word:
                            word = word.strip()
                            word = word[3:].strip()
                            functions.append(word)
                        if "rule" in word: 
                            activation = True
                        word = ""

        regex = list(filter(bool, regex))

        for x in range(len(regex)):
            temporary_array = []
            temporary_word = ""
            token_active = False
            
            for l in regex[x]:
                if token_active:
                    if l == "}":
                        temporary_word = temporary_word.replace("'","").replace('"',"").strip()
                        temporary_array.append(temporary_word)
                        token_regex.append(temporary_array[0])
                        token_regex.append("|")
                        temporary_word = ""
                        token_functions.append(temporary_array)
                        break
                    temporary_word += l
                else:
                    temporary_word += l
                if l == "{":
                    temporary_word = temporary_word[:-1].replace("'","").replace('"',"").strip()
                    temporary_array.append(temporary_word)
                    temporary_word = ""
                    token_active = True

            if temporary_word and "|" not in temporary_word and len(temporary_word) > 0:
                temporary_word = temporary_word.strip()
                temporary_array.append(temporary_word)
                temporary_array.append("")
                token_regex.append(temporary_array[0])
                token_regex.append("|")
                token_functions.append(temporary_array)


        token_regex.pop()

        for x in range(len(regex)):
            temporary_word = ""
            for l in regex[x]:
                temporary_word += l
                if "{" in temporary_word:
                    temporary_word = temporary_word[:-1].strip()
                    break 
                if "(*" in temporary_word :
                    if temporary_word[0] == "(":
                        temporary_word = temporary_word[:-2].strip()
                        break 
            if temporary_word.count("'") == 2 or temporary_word.count('"') == 2:
                temporary_word = temporary_word[1:-1]

            regex[x] = temporary_word
        
        for x in regex:
            if len(x) != 0:
                if x.count('"') == 2:
                    x = x[1:-1]
                filter_regex.append(x)


        for f in functions:
            deletable_array = []
            temporal_array = []
            nombre, definicion = f.split("=")

            nombre = nombre.strip()
            definicion = definicion.strip()
            temporal_array.append(nombre)
            word= ""

            if definicion[0] == "[":
                definicion = definicion[1:-1]
                for x in definicion:
                    word+=x
                    if word[0] == '"' or word[0] == "'":
                        if word.count("'") == 2:
                            word = word[1:-1]
                            if len(word) == 2:
                                if word == "\s":
                                    word = bytes(' ', 'utf-8').decode('unicode_escape')
                                else:
                                    word = bytes(word, 'utf-8').decode('unicode_escape')
                                deletable_array.append(ord(word))
                            else:
                                if word == " ":
                                    word = bytes(' ', 'utf-8').decode('unicode_escape')
                                    deletable_array.append(ord(word))
                                else:
                                    deletable_array.append(ord(word))
                            word = ""
                        if word.count('"') == 2:
                            word = word[1:-1]
                            temporary_word = ""
                            if chr(92) in word:
                                for y in word:
                                    temporary_word+=y
                                    if temporary_word.count(chr(92)) == 2:
                                        if temporary_word[:-1] == "\s":
                                            temp_word = ' '
                                        else:
                                            temp_word = temporary_word[:-1]
                                        
                                        word = bytes(temp_word, 'utf-8').decode('unicode_escape')
                                        deletable_array.append(ord(word))
                                        temporary_word = temporary_word[2:]
                                if len(temporary_word) != 0:
                                    if temporary_word == "\s":
                                        temp_word = ' '
                                    else:
                                        temp_word = temporary_word
  
                                    word = bytes(temp_word, 'utf-8').decode('unicode_escape')
                                    deletable_array.append(ord(word))
                            else:
                                word = list(word)
                                for w in range(len(word)):
                                    word[w] = ord(word[w])
                                deletable_array.extend(word)
                                
                    else:
                        deletable_array.append(word)
                        word = ""
                
                
            else:
                tokens = []
                token_actual = ""
                
                for caracter in definicion:
                    
                    if "]" in token_actual:
                        palabra = ""
                        array = []
                        array.append("(")
                        
                        token_actual = token_actual[1:-1]
                        for tok in token_actual:
                            palabra += tok
                            if palabra.count("'") == 2:
                                palabra = ord(palabra[1:-1])
                                array.append(palabra)
                                array.append("|")
                                palabra = ""
                        array[len(array)-1] = ")"
                        tokens.extend(array)
                        token_actual = ""
                    
                    if token_actual.count("'") == 2:
                        if "[" not in token_actual:
                            token_actual = ord(token_actual[1:-1])
                            tokens.append(token_actual)
                            token_actual = ""
                    
                    if caracter in ("(", ")", "*", "?", "+", "|","."):
                        if "'" not in token_actual:
                            if token_actual:
                                if len(token_actual) == 1:
                                    token_actual = ord(token_actual)
                                tokens.append(token_actual)
                                token_actual = ""
                            if caracter == ".":
                                caracter = ord(caracter)
                            tokens.append(caracter)
                        else:
                            token_actual += caracter.strip()
                    else:
                        token_actual += caracter.strip()
                if token_actual:
                    tokens.append(token_actual)
                deletable_array.extend(tokens)
                
                
            temporal_array.append(deletable_array)
            
            filter_functions.append(temporal_array)

        for x in range(len(filter_functions)):
            isFunc = True
            
            for c in ["+","*","(",")","?","|"]:
                if c in filter_functions[x][1]:
                    isFunc = False
                
            
            if isFunc == False:
                
                temporal_array = []
                for y in filter_functions[x][1]:
                    temporal_array.append(y)
                    temporal_array.append("•")
                for z in range(len(temporal_array)):
                    if temporal_array[z] == "(":
                        if temporal_array[z+1] == "•":
                            temporal_array[z+1] = ''
                    if temporal_array[z] == ")":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                    if temporal_array[z] == "*":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                    if temporal_array[z] == "|":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                        if temporal_array[z+1] == "•":
                            temporal_array[z+1] = ''
                    if temporal_array[z] == "+":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                    if temporal_array[z] == "?":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                temporal_array = [element for element in temporal_array if element != '']
                            
                filter_functions[x][1] = temporal_array[:-1]
                
            else:
                ascii_array=[]
                newString_Array = []
                if '-' in filter_functions[x][1]:
                    for z in range(len(filter_functions[x][1])):
                        if filter_functions[x][1][z] == '-':
                            for i in range(filter_functions[x][1][z-1],filter_functions[x][1][z+1]+1):
                                ascii_array.append(i)
                    for i in ascii_array:
                        newString_Array.append(i)
                    filter_functions[x][1] = newString_Array

                newString_Array = []
                for y in filter_functions[x][1]:
                    newString_Array.append(y)
                    newString_Array.append('|')
                    
                newString_Array = newString_Array[:-1]
                filter_functions[x][1] = newString_Array
                
        for func in filter_functions:
            func[1].insert(0,"(")
            func[1].insert(len(func[1]),")")

        functionNames = []

        for x in filter_functions:
            functionNames.append(x[0])
        functionNames.append('|')

        for x in range(len(filter_regex)):
            if filter_regex[x] not in functionNames:
                if len(filter_regex[x]) == 1:
                    filter_regex[x] = ord(filter_regex[x])
            if filter_regex[x] == "|" and filter_regex[x-1] == "|":
                filter_regex[x] = ord(filter_regex[x])
                

        temporalNewRegex = []
        for x in range(len(filter_regex)):
            if filter_regex[x] != "|":
                temporalNewRegex.append("(")
                temporalNewRegex.append(filter_regex[x])
                temporalNewRegex.append("•")
                temporalNewRegex.append("#"+str(token_regex[x]))
                temporalNewRegex.append(")")
            else:
                temporalNewRegex.append(filter_regex[x])
        
        filter_regex = temporalNewRegex

        final_regex = []
        
        for token in filter_regex:
            exists = False
            for f in filter_functions:
                if token == f[0]:
                    exists = True
                    temp_regex = []
                    temp_regex.extend(f[1])
                    length = 0
                    while (length != len(temp_regex)):
                                    
                        length = len(temp_regex)
                        i = 0
                        check_regex = []
                        while (i < len(temp_regex)):
                            validation = False
                            for x in filter_functions:
                                if temp_regex[i] == x[0]:
                                    validation = True
                                    check_regex.extend(x[1])
                                    check_regex.extend(temp_regex[i+1:])
                                    temp_regex = check_regex
                                    i = len(temp_regex)
                                    check_regex = []
                                    break

                            if validation == False:
                                check_regex.append(temp_regex[i])
                                i+=1
                            
                    final_regex.extend(temp_regex)
                    
            if exists == False:
                if isinstance(token, str):
                    if len(token) > 1:
                        if '#' not in token:

                            temporal = []
                            temporal.append("(")
                            for i in token:
                                temporal.append(ord(i))
                                temporal.append("•")
                            temporal.pop(len(temporal)-1)
                            temporal.append(")")

                            final_regex.extend(temporal)
                        else:
                            final_regex.append(token)
                    else:
                        final_regex.append(token)
                else:
                    final_regex.append(token)

        return final_regex,token_functions