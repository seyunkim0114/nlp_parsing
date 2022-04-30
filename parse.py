# from CFG_to_CNF.py import *

# Store grammar rules specified in grammar_file in python dictionary
def load_grammar(grammar_file):
    rules = {}
    with open(grammar_file, 'r') as f:
        for line in f:
            line = line.split()
            
            head = line[0]
            tail = ' '.join(line[2:])

            if tail in rules.keys():
                rules[tail].append(head)
            else:
                rules[tail] = [head]

    f.close()

    return rules

def is_valid_sentence(cyk_cell):
    for cell in cyk_cell:
        if cell.head == "S":
            return True
    return False

class Node:
    def __init__(self, head, t1, t2 = None):
        self.head = head
        self.t1 = t1
        self.t2 = t2

def parse_sentence(node):
    # is terminal
    if node.t2 == None:
        parsed = "[" + node.head + " " + node.t1 + "]"
    else:
        parsed = "[" + node.head + " " + parse_sentence(node.t1) + " " + parse_sentence(node.t2) + "]"
    
    return parsed
    
def parse_tree_sentence(node, s):
    if node.t2 == None:
        parsed = "[" + node.head + " " + node.t1 + "]"
    else:
        s += "  "
        parsed = "[" + node.head + "\n" + s + parse_tree_sentence(node.t1, s) + "\n" + s + parse_tree_sentence(node.t2, s) + "\n" + s[:-2] + "]"
    # if node.t2 == None:
    #     parsed = "[" + node.head + " " + node.t1 + "]"
    # else:
    #     parsed = "[" + node.head + "\n  " + parse_tree_sentence(node.t1)
    
    # if node.t2 == None:
    #     s += "  "
    #     parsed = s + "[" + node.head + " " + node.t1 + "]"
    # else:
    #     parsed  = "[" + node.head + "\n" + s + parse_tree_sentence(node.t1) + "\n" + s + parse_tree_sentence(node.t2) + "  \n]"
        
    return parsed

def recognize_sentence(sentence, rules, draw_tree):
    w = sentence.split()

    n = len(w)

    cyk_table = [[[] for i in range(n)] for j in range(n)]

    # fill in first row
    for i in range(n):
        if w[i] in rules.keys():
            for rule in rules[w[i]]:
            # cyk_table[i][i] = rules[w[i]]
                cyk_table[i][i].append(Node(rule, w[i]))
        else:
            pass

    # fill in other cells
    for l in range(2, n+1): # l = # of constituents
        for i in range(n-l+1): # i = number of "slides" 
            j = i+l-1 # j = last index of current constituent
            # print(j)
            for k in range(i, j): # loop through constituents
                first = cyk_table[i][k]
                # print(f'first {i},{k} : {first}')
                # print(first[0])
                second = cyk_table[k+1][j]
                # print(f'second {k+1},{j} : {second}')

                for f in first:
                    for s in second:
                        tail = f.head + " " + s.head
                        if tail in rules.keys():
                            for rule in rules[tail]:
                                cyk_table[i][j].append(Node(rule, f, s))
                        else:
                            pass

    # for i in cyk_table[0][-1]:
    #     print(i.head)

    if is_valid_sentence(cyk_table[0][-1]):
        print("VALID SENTENCE\n")

        parsed_sentences = []
        for cell in cyk_table[0][-1]:
            if cell.head == "S":
                parsed_sentences.append(parse_sentence(cell))
            else:
                pass

        for i, p in enumerate(parsed_sentences):
            print(f'Valid parse #{i+1}')
            print(p + "\n")

        if draw_tree == 'y':
            s = ""
            b = ""
            for i, cell in enumerate(cyk_table[0][-1]):
                if cell.head == "S":
                    print(f'Valid parse tree #{i+1}')
                    print(parse_tree_sentence(cell, s) + "\n")
                else:
                    pass
        else: 
            pass

        print(f'Number of valid parses: {len(parsed_sentences)}')

        return 0

    else:
        print("NO VALID PARSES")
        return 0



grammar_file = input("Enter the name of a text file specifying a CFG in CNF: ")
# grammar_file = "sampleGrammar.cnf.txt"
print("Loading grammar...")
draw_tree = input("Do you want textual parse trees to be displayed (y/n)?: ")

rules = load_grammar(grammar_file)

# diplay_parse_tree = input("Do you want textual aprse trees to be displayed (y/n)? ")
sentence = input("Enter a sentence to parse. To quit, type 'quit': ")
while sentence != 'quit':

    recognize_sentence(sentence, rules, draw_tree)
    sentence = input("Enter a sentence to parse. To quit, type 'quit': ")


