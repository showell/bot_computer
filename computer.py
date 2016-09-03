from parser import parse

def make_arg(token):
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
        self.token = token
        tokens = token.tokens[:]
        action = tokens.pop(0)
        assert action.kind == 'literal'
        self.action = str(action)
        self.args = [make_arg(t) for t in tokens]

    def compute(self):
        return send_calculation(self.token)

class BuiltinBot:
    def __init__(self, name, compute_via_python):
        self.name = name
        self.compute_via_python = compute_via_python

    def receive(self, message):
        token = parse(message)
        assert token.kind == 'expression'
        calculation = Calculation(token)
        if calculation.action != self.name:
            print str(token)
            print calculation.action
            raise Exception('Wrong bot dispatched.')
        computed_args = [a.compute() for a in calculation.args]
        return self.compute_via_python(computed_args)

def multiply(args):
    product = 1
    for arg in args:
        product = int(arg) * product
    return product

BOTS = {
    'ADD': BuiltinBot(
        name='ADD',
        compute_via_python = lambda args:
            sum(int(x) for x in args)
    ),
    'MULT': BuiltinBot(
        name='MULT',
        compute_via_python = lambda args:
            multiply(args)
    ),
}

class Human:
    def receive(self, message):
        # For now we will do our own computations
        token = parse(message)
        assert token.kind == 'expression'
        calculation = Calculation(token)
        answer = send_calculation(token)
        print '%s -> %s' % (message, answer)

def send_message(agent, message):
    return agent.receive(message)

def send_calculation(token):
    # generalize
    message = str(token)
    action = str(token.tokens[0])
    bot = BOTS[action]
    return send_message(bot, message)

def run():
    human = Human()
    message = '[ADD 8 [MULT 10 6]]'
    send_message(human, message)

if __name__ == '__main__':
    run()
