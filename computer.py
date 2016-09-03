def tokenize(s):
    res = []
    i = 0
    t = ''
    for i, c in enumerate(s):
        if c in '[] ':
            if t:
                res.append(t)
            if c != ' ':
                res.append(c)
            t = ''
        else:
            t += c
    if t:
        res.append(t)
    return res

class LiteralToken:
    def __init__(self, s):
        self.s = s
        self.kind = 'literal'

    def __str__(self):
        return self.s

class ExpressionToken:
    def __init__(self, tokens):
        self.tokens = tokens
        self.kind = 'expression'

    def __str__(self):
        return '[' + ' '.join(str(t) for t in self.tokens) + ']'

def parse(s):
    tokens = tokenize(s)

    def _parse_bracket_expr(tokens):
        tokens = tokens[1:]
        res = []
        while True:
            if not tokens:
                raise Exception('unclosed bracket')
            if tokens[0] == ']':
                return ExpressionToken(res), tokens[1:]
            else:
                head, rest = _parse(tokens)
                assert head
                res.append(head)
                tokens = rest

    def _parse(tokens):
        if not tokens:
            return None, None
        if tokens[0] == '[':
            return _parse_bracket_expr(tokens)
        else:
            return LiteralToken(tokens[0]), tokens[1:]


    lst, rest = _parse(tokens)
    assert rest == []
    return lst

def make_args(token):
    if token.kind == 'literal':
        return Literal(token)
    else:
        return Calculation(token)

class Literal:
    def __init__(self, token):
        self.s = str(token)

    def compute(self):
        return self.s

class Calculation:
    def __init__(self, token):
        action = token.tokens.pop(0)
        assert action.kind == 'literal'
        self.action = str(action)
        self.args = [make_args(t) for t in token.tokens]

    def compute(self):
        pass

class Bot:
    def __init__(self, name, compute_via_python):
        self.name = name
        self.compute_via_python = compute_via_python

    def receive(self, message):
        token = parse(message)
        assert token.kind == 'expression'
        calculation = Calculation(token)
        if calculation.action != self.name:
            raise Exception('Wrong bot dispatched.')
        computed_args = [a.compute() for a in calculation.args]
        return self.compute_via_python(computed_args)

BOTS = {
    'ADD': Bot(
        name='ADD',
        compute_via_python = lambda args:
            sum(int(x) for x in args)
    ),
}

class Human:
    def receive(self, message):
        # For now we will do our own computations
        token = parse(message)
        assert token.kind == 'expression'
        calculation = Calculation(token)
        answer = send_calculation(calculation, message)
        print '%s -> %s' % (message, answer)

def send_message(agent, message):
    return agent.receive(message)

def send_calculation(calculation, message):
    # generalize
    return send_message(BOTS['ADD'], message)

def run():
    human = Human()
    message = '[ADD 8  2 1]'
    send_message(human, message)

if __name__ == '__main__':
    run()
