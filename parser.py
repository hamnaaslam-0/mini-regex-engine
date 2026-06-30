
def preprocess_regex(regex: str) -> str:
    output = []
    infix_op = {'|', '('}
    postfix_op = {'*', '+', '?', ')', '|'}

    for i in range(len(regex)):
        curr_char = regex[i]
        output.append(curr_char)

        if i + 1 < len(regex):
            next_char = regex[i + 1]
            is_curr_operand = (curr_char not in infix_op)
            is_next_operand = (next_char not in postfix_op)

            if is_curr_operand and is_next_operand:
                output.append('&')
    return "".join(output)


def regex_to_postfix(regex: str) -> str:
    preprocessed = preprocess_regex(regex)
    precedence = {
        '*': 4, '+': 4, '?': 4,
        '&': 3,
        '|': 2,
        '(': 1
    }

    output_queue = []
    operator_stack = []

    for char in preprocessed:
        if char == '(':
            operator_stack.append(char)
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack:
                operator_stack.pop()
        elif char in precedence:
            while (operator_stack and
                   precedence[operator_stack[-1]] >= precedence[char]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(char)
        else:
            output_queue.append(char)

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return "".join(output_queue)
