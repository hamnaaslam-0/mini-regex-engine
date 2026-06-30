class State:
    def __init__(self):
        self.edges = {}
        self.epsilon = []

class Fragment:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept


def build_nfa(postfix: str) -> Fragment:
    stack = []

    for char in postfix:
        if char == '&':
            frag2 = stack.pop()
            frag1 = stack.pop()
            frag1.accept.epsilon.append(frag2.start)
            stack.append(Fragment(frag1.start, frag2.accept))

        elif char == '|':
            frag2 = stack.pop()
            frag1 = stack.pop()
            start = State()
            accept = State()
            start.epsilon.extend([frag1.start, frag2.start])
            frag1.accept.epsilon.append(accept)
            frag2.accept.epsilon.append(accept)
            stack.append(Fragment(start, accept))

        elif char == '*':
            frag = stack.pop()
            start = State()
            accept = State()
            start.epsilon.extend([frag.start, accept])
            frag.accept.epsilon.extend([frag.start, accept])
            stack.append(Fragment(start, accept))

        elif char == '+':
            frag = stack.pop()
            start = State()
            accept = State()
            start.epsilon.append(frag.start)
            frag.accept.epsilon.extend([frag.start, accept])
            stack.append(Fragment(start, accept))

        elif char == '?':
            frag = stack.pop()
            start = State()
            accept = State()
            start.epsilon.extend([frag.start, accept])
            frag.accept.epsilon.append(accept)
            stack.append(Fragment(start, accept))

        else:
            start = State()
            accept = State()
            start.edges[char] = [accept]
            stack.append(Fragment(start, accept))

    return stack.pop()
