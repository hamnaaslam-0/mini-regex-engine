# Mini Regex Engine

A regex engine built from scratch in Python, implementing the core theory behind regular expression matching — from parsing a pattern, to building an NFA, converting it to a DFA, minimizing the DFA, and simulating it against input strings.

Built as a group project for a Theory of Computation course.

## How It Works

The pipeline follows these stages:

1. **Parser** (`parser.py`) — parses the regex pattern into a usable internal representation
2. **NFA Construction** (`nfa.py`) — builds a Non-deterministic Finite Automaton from the parsed pattern
3. **DFA Conversion** (`dfa.py`) — converts the NFA to a Deterministic Finite Automaton via subset construction
4. **DFA Minimization** (`minimizer.py`) — reduces the DFA to its minimal equivalent form using Hopcroft's algorithm
5. **Simulation** (`simulator.py`) — runs the final DFA against input strings to test for matches

## My Contribution

This was a group project (4 members). My specific contributions:

- Implemented DFA minimization (`minimizer.py`) using Hopcroft's algorithm, reducing redundant states while preserving language equivalence
- Compiled the full project report, documenting the theory and implementation behind NFA/DFA construction, subset construction, and minimization with worked examples

## Team

Built with teammates: Roha, Meer Umar, and Wasif

## Concepts Demonstrated

NFA construction · DFA conversion (subset construction) · DFA minimization (Hopcroft's algorithm) · Automata simulation
