import nltk
from nltk.tokenize import word_tokenize

test_sent = "The book on the table is mine"

grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | NP PP | N
VP -> V NP | VP PP
Det -> 'a' | 'The' | 'the'
N -> 'I' | 'chicken' | 'kitchen' | 'book' | 'table' | 'mine'
V -> 'kill' | 'is'
P -> 'in' | 'on'
""")

word_list = word_tokenize(test_sent)

print(word_list)

parser = nltk.ChartParser(grammar)
for t in parser.parse(word_list):
    t.draw()
