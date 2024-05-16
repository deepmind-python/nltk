import nltk
from nltk.tokenize import word_tokenize

test_sent = "The Toyota was red before the police stopped"
             

grammar = nltk.CFG.fromstring("""
S -> NP VP
ADVC -> CONJ S
NP -> Det N | N
ADJP -> ADJ
VP -> V ADJP | V ADJP ADVC | V
Det -> 'The' | 'the'
N -> 'Toyota' | 'police' 
V -> 'was' | 'stopped'
ADJ -> 'red'
CONJ -> 'before'                             
""")

word_list = word_tokenize(test_sent)

print(word_list)

parser = nltk.ChartParser(grammar)
for t in parser.parse(word_list):
    t.draw()


