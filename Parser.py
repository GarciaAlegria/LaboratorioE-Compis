import copy
import pandas as pd
from tabulate import tabulate

class Parser(object):
    def __init__(self, transitions, sets, numbers, rules):
        self.transitions = transitions
        self.sets = sets
        self.rules = rules
        self.not_terminals = []
        
        self.state = numbers
        self.first = []
        self.action_rows = []
        self.action = []
        self.goto_rows = []
        self.goto = []
        
        for token in self.rules:
            if token[0] not in self.not_terminals:
                self.not_terminals.append(token[0])
                
    def construct_table(self):
        self.goto_rows = sorted(list(set(x[1] for x in self.transitions if x[1].isupper())))
        self.action_rows = sorted(list(set(x[1] for x in self.transitions if not x[1].isupper())), reverse=True)

        def find_transitions(state, symbol):
            return [(x[0], x[1], x[2]) for x in self.transitions if x[0] == state and x[1] == symbol]

        for state in self.state:
            for symbol in self.goto_rows:
                self.goto.extend(find_transitions(state, symbol))
            for symbol in self.action_rows:
                self.action.extend(find_transitions(state, symbol))

        first = self.rules[0][1][0]

        for rule in self.rules:
            visited = [rule[0]]
            for y in visited:
                new_visited = [z[1][0] for z in self.rules if y == z[0] and z[1][0] not in visited]
                visited.extend(new_visited)

            self.first.append([rule[0], sorted(list(set(y for y in visited if y in self.action_rows)))])

        for i, state in enumerate(self.sets):
            for item in state:
                if item[1][-1] == ".":
                    index = item[1].index(".")
                    if item[1][index - 1] != first:
                        trans_copy = copy.deepcopy(item)
                        trans_copy[1].remove(".")
                        for j, rule in enumerate(self.rules):
                            if rule == trans_copy:
                                transaction = self.follow(trans_copy[0], first)
                                self.action.extend([(i, w, "r" + str(j)) for w in transaction])

        print("FIRST: ", self.first)
        print("GOTO: ", self.goto)
        print("ACTION: ", self.action)


        
    def follow(self, state, accept_state):
        accept_state += "'"
        revisar = {state}

        while True:
            new_revisar = set()
            for y in revisar:
                for x in self.rules:
                    if y in x[1]:
                        index = x[1].index(y)
                        if index == len(x[1]) - 1:
                            new_revisar.add(x[0])
                        elif index + 1 < len(x[1]) and x[1][index + 1] in self.not_terminals:
                            first_values = [z[1] for z in self.first if z[0] == x[1][index + 1]]
                            new_revisar.update(first_values[0] if first_values else [])

            if len(revisar) == len(revisar | new_revisar):
                break

            revisar |= new_revisar

        transactions = set()
        for x in revisar:
            for y in self.rules:
                if x in y[1]:
                    index = y[1].index(x)
                    if index + 1 < len(y[1]) and y[1][index + 1] not in self.not_terminals:
                        transactions.add(y[1][index + 1])

        if accept_state in revisar:
            transactions.add("$")

        return list(transactions)


    def draw_table(self):
        columns = self.action_rows + self.goto_rows
        df = pd.DataFrame(columns=columns)

        for row, col, value in self.goto + self.action:
            df.at[row, col] = value

        df.fillna('', inplace=True)

        df.index.name = 'state'

        headers = ['ACTION'] * len(self.action_rows) + ['GOTO'] * len(self.goto_rows)
        df.columns = pd.MultiIndex.from_tuples(zip(headers, df.columns))
        
        df.sort_index(inplace=True)
        
        table = tabulate(df, headers='keys', tablefmt='heavy_grid', showindex=True)
        print(table)