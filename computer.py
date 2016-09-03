from parser import parse

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
        self.token = token
        tokens = token.tokens[:]
        action = tokens.pop(0)
        assert action.kind == 'literal'
        self.action = str(action)
        self.args = [make_args(t) for t in tokens]

    def compute(self):
        return send_calculation(self.token)

class Bot:
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
        answer = send_calculation(token)
        print '%s -> %s' % (message, answer)

def send_message(agent, message):
    return agent.receive(message)

def send_calculation(token):
    # generalize
    message = str(token)
    print message
    return send_message(BOTS['ADD'], message)

def run():
    human = Human()
    message = '[ADD 9 1]'
    message = '[ADD 8 [ADD 2 1]]'
    send_message(human, message)

if __name__ == '__main__':
    run()
