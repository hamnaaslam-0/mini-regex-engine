from engine.dfa import DFAState

def minimize_dfa(dfa_states, alphabet, verbose=False):
    if not dfa_states:
        if verbose:
            print("\n--- Stage 4: Minimization Report ---")
            print("States before minimization: 0")
            print("States after minimization : 0")
            print("Reduction percentage      : 0.00%")
            print("------------------------------------------------\n")
        return []

    total_states_before = len(dfa_states)
    accepting = set(s for s in dfa_states if s.is_accept)
    non_accepting = set(s for s in dfa_states if not s.is_accept)

    partitions = []
    if accepting:
        partitions.append(frozenset(accepting))
    if non_accepting:
        partitions.append(frozenset(non_accepting))

    if verbose:
        print("\n>>> Stage 4: Partition Evolution Tracing <<<")
        initial_p_str = ", ".join(f"{{{[s.id for s in group]}}}" for group in partitions)
        print(f"  Iteration 0 (Initial Groups) : {initial_p_str}")

    changed = True
    iteration_counter = 1

    while changed:
        changed = False
        new_partitions = []

        for group in partitions:
            if len(group) <= 1:
                new_partitions.append(group)
                continue

            splits = {}
            for state in group:
                signature = []
                for symbol in sorted(alphabet):
                    target = state.transitions.get(symbol)
                    target_group_idx = -1
                    if target:
                        for idx, p_group in enumerate(partitions):
                            if target in p_group:
                                target_group_idx = idx
                                break
                    signature.append((symbol, target_group_idx))

                signature_key = tuple(signature)
                if signature_key not in splits:
                    splits[signature_key] = set()
                splits[signature_key].add(state)

            if len(splits) > 1:
                changed = True
            for split_set in splits.values():
                new_partitions.append(frozenset(split_set))

        if changed:
            partitions = new_partitions
            if verbose:
                p_str = ", ".join(f"{{{[s.id for s in group]}}}" for group in partitions)
                print(f"  Iteration {iteration_counter} (Refined Split)  : {p_str}")
                iteration_counter += 1
        else:
            partitions = new_partitions

    state_map = {}
    minimized_states = []

    for idx, group in enumerate(partitions):
        new_state = DFAState(idx, set())
        new_state.is_accept = any(s.is_accept for s in group)
        minimized_states.append(new_state)
        for original_state in group:
            state_map[original_state] = new_state

    for original_state, new_state in state_map.items():
        for symbol, target in original_state.transitions.items():
            if target in state_map:
                new_state.transitions[symbol] = state_map[target]

    start_state = None
    for original_state, new_state in state_map.items():
        if original_state.id == 0:
            start_state = new_state
            break

    if start_state and start_state.id != 0:
        old_zero = next(s for s in minimized_states if s.id == 0)
        old_zero.id, start_state.id = start_state.id, 0

    minimized_states.sort(key=lambda s: s.id)
    total_states_after = len(minimized_states)
    reduction_pct = ((total_states_before - total_states_after) / total_states_before) * 100

    if verbose:
        print(f"\n--- Stage 4: Minimization Report ---")
        print(f"States before minimization: {total_states_before}")
        print(f"States after minimization : {total_states_after}")
        print(f"Reduction percentage      : {reduction_pct:.2f}%")
        print("------------------------------------------------\n")

    return minimized_states
