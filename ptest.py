import hermes.extraction.tre as tre
import hermes.core as core

stack = []

nfa = tre.compile("(?<NP> ~ #NOUN)")

d = core.Document('This is a no go for you man?')
d.annotate('token')
tt = d.tokens()
index = 0
while index < len(tt):
    ni = nfa.match(d, index)
    if ni > 0:
        print(d[tt[index].start:tt[ni - 1].end])
    index = index + 1 if ni < 0 else ni
