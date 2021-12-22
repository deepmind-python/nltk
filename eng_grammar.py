import nltk

grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | NP PP | N 
VP -> V NP | VP PP
Det -> 'an' | 'a' | 'The' | 'the'
N -> 'elephant' | 'room' | 'kitchen' | 'chicken' | 'monkey'| 'table'| 'banana'|'I'
V -> 'kill' | 'eat' | 'eats'
P -> 'in' | 'on'
 """)

sent1 = ['I', 'kill', 'a', 'chicken', 'in', 'a', 'kitchen']
sent2 = ['The', 'monkey', 'eats', 'a', 'banana', 'on', 'a', 'table']

parser = nltk.ChartParser(grammar)

treegraph = []

for t in parser.parse(sent2):
    print(t, end='\n\n\n')  
    treegraph.append(t)
    t.draw()


        

    



    
    
    
    