import nltk
from nltk.tokenize import word_tokenize

test_sent = "I kill a chicken in a kitchen"

grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | NP PP | N
VP -> V NP | VP PP
Det -> 'a'
N -> 'I' | 'chicken' | 'kitchen'
V -> 'kill'
P -> 'in'
""")

word_list = word_tokenize(test_sent)

print(word_list)

parser = nltk.ChartParser(grammar)
for t in parser.parse(word_list):
    t.draw()
