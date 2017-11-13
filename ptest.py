import hermes.extraction.tre as tre
import hermes.core as core

stack = []

nfa = tre.compile("#NOUN")

d = core.Document('What time is it in London?')
d.annotate('token')
tt = d.tokens()
index = 0
for t in d.tokens():
    print("%s/%s" % (t, t.pos()), end=' ')
print()
while index < len(tt):
    ni = nfa.match(d, index)
    if ni > 0:
        print(d[tt[index].start:tt[ni - 1].end])
    index = index + 1 if ni < 0 else ni
