class NFANode:
    def __init__(self, accept=False, consumes=False, emits=False, name=None):
        self.accept = accept
        self.name = name
        self.emits = emits
        self.consumes = consumes
        self.transitions = []
        self.epsilons = []

    def __str__(self) -> str:
        return '(Node: %s transitions, %s epsilons, accept=%s)' % (
            len(self.transitions), len(self.epsilons), self.accept)

    def __repr__(self) -> str:
        return str(self)

    def connect(self, node, transition_function=None):
        if transition_function:
            self.transitions.append((self, node, transition_function))
        else:
            self.epsilons.append(node)


class NFA:
    def __init__(self):
        self.start = NFANode()
        self.end = NFANode(True)

    def match(self, hstr, start_index=0):
        from collections import deque
        states = []
        accept_states = deque()
        states.append(NFAState(index=start_index, node=self.start))

        tokens = hstr.tokens()

        while len(states) > 0:
            new_states = []
            for s in states:
                if s.node.accept:
                    if len(s.stack) == 0 or (len(s.stack) == 1 and s.node.consumes and s.node.name == s.stack[0][0]):
                        accept_states.append(s)

                current_stack = s.stack
                if s.node.emits:
                    current_stack.insert(0, (s.node.name, s.index))

                for n in s.node.epsilons:
                    next = NFAState(s.index, n, current_stack)
                    new_states.append(next)

                if s.index >= len(tokens):
                    continue

                for t in s.node.transitions:
                    l = t[2].matches(tokens[s.index])
                    if l > 0:
                        next = NFAState(s.index + l, t[1])
                        new_states.append(next)

            states = new_states

        max = None
        for a in accept_states:
            if max:
                if a.index > max.index:
                    max = a
            else:
                max = a

        return max.index if max else -1


class NFAState:
    def __init__(self, index, node, stack=None):
        self.index = index
        self.node = node
        self.stack = stack if stack else []


class Transition:
    def matches(self, hStr) -> int:
        raise NotImplementedError

    def not_matches(self, hStr) -> int:
        raise NotImplementedError

    def construct(self) -> NFA:
        nfa = NFA()
        nfa.start.connect(nfa.end, self)
        return nfa
