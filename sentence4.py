import nltk
from nltk.tokenize import word_tokenize

test_sent = "The monkey eats a banana on a table in a room"

grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | NP PP | N
VP -> V NP | VP PP
Det -> 'an' |'a' |'The' |'the'
N -> 'kitchen' |'chicken' |'monkey' |'table' |'banana' |'I' |'man' |'telescope' |'room'
V -> 'is' | 'eat' | 'eats' | 'kill' | 'saw'
P -> 'in' | 'on' | 'with'
""")

word_list = word_tokenize(test_sent)

print(word_list)

parser = nltk.ChartParser(grammar)
for t in parser.parse(word_list):
    t.draw()
