from engine.nfa import Fragment


class DFAState:
    def __init__(self, state_id, nfa_set):
        self.id = state_id
        self.nfa_set = nfa_set
        self.transitions = {}
        self.is_accept = False


def compute_epsilon_closure(states):
    stack = list(states)
    closure = set(states)

    while stack:
        current = stack.pop()
        for next_state in current.epsilon:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure


def compute_move(states, symbol):
    moved_set = set()
    for state in states:
        if symbol in state.edges:
            for next_state in state.edges[symbol]:
                moved_set.add(next_state)
    return moved_set


def build_dfa(nfa_fragment: Fragment):
    alphabet = set()
    visited = set()
    stack = [nfa_fragment.start]

    while stack:
        curr = stack.pop()
        if curr not in visited:
            visited.add(curr)
            for symbol in curr.edges.keys():
                alphabet.add(symbol)
            for next_state in curr.epsilon:
                stack.append(next_state)
            for next_states in curr.edges.values():
                stack.extend(next_states)

    dfa_states = []
    nfa_set_to_dfa = {}

    start_closure = compute_epsilon_closure({nfa_fragment.start})
    start_frozen = frozenset(start_closure)

    state_id_counter = 0
    dfa_start = DFAState(state_id_counter, start_closure)
    state_id_counter += 1

    dfa_states.append(dfa_start)
    nfa_set_to_dfa[start_frozen] = dfa_start

    unprocessed_queue = [dfa_start]

    while unprocessed_queue:
        current_dfa = unprocessed_queue.pop(0)

        if nfa_fragment.accept in current_dfa.nfa_set:
            current_dfa.is_accept = True

        for symbol in alphabet:
            move_result = compute_move(current_dfa.nfa_set, symbol)
            closure_result = compute_epsilon_closure(move_result)

            if not closure_result:
                continue

            frozen_closure = frozenset(closure_result)

            if frozen_closure not in nfa_set_to_dfa:
                new_dfa_state = DFAState(state_id_counter, closure_result)
                state_id_counter += 1
                dfa_states.append(new_dfa_state)
                nfa_set_to_dfa[frozen_closure] = new_dfa_state
                unprocessed_queue.append(new_dfa_state)

            current_dfa.transitions[symbol] = nfa_set_to_dfa[frozen_closure]

    return dfa_start, dfa_states
