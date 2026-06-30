from typing import Tuple, List

def simulate_min_dfa(min_dfa_start_state, input_str: str, verbose: bool = False) -> Tuple[bool, List[str]]:
    if not min_dfa_start_state:
        return False, ["Error: Missing engine entry configuration."]

    current = min_dfa_start_state
    steps_log = []

    for char in input_str:
        next_state = current.transitions.get(char, None)

        if next_state is None and '.' in current.transitions:
            next_state = current.transitions['.']

        if next_state is None:
            if verbose:
                steps_log.append(f"| State {current.id:<11} | '{char}':<12 | REJECT / DEAD     |")
            return False, steps_log

        if verbose:
            steps_log.append(f"| State {current.id:<11} | '{char}':<12 | State {next_state.id:<13} |")
        current = next_state

    return current.is_accept, steps_log


def run_substring_search(min_dfa_start_state, text: str) -> Tuple[bool, int, int]:
    n = len(text)
    for start in range(n + 1):
        for end in range(start, n + 1):
            substring_candidate = text[start:end]
            matched, _ = simulate_min_dfa(min_dfa_start_state, substring_candidate, verbose=False)
            if matched:
                return True, start, end
    return False, -1, -1
