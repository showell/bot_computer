from parser import parse
from builtin import make_builtin_bots

def make_arg(token):
    if token.kind == 'literal':
        return Literal(token)
    else:
        return Calculation(token)

class Literal:
    def __init__(self, token):
        self.s = str(token)

    def compute(self, callback):
        callback(self.s)

class Calculation:
    def __init__(self, token):
        self.token = token
        tokens = token.tokens[:]
        action = tokens.pop(0)
        assert action.kind == 'literal'
        self.action = str(action)
        self.args = [make_arg(t) for t in tokens]

    def compute(self, callback):
        send_calculation(callback, self.token)

    def compute_args(self, callback):
        computed_args = []

        def on_computed_arg(computed_arg):
            computed_args.append(computed_arg)
            compute_one()

        def compute_one():
            if len(computed_args) == len(self.args):
                callback(computed_args)
            else:
                arg = self.args[len(computed_args)]
                arg.compute(on_computed_arg)

        compute_one()

class BuiltinBot:
    def __init__(self, name, compute_via_python):
        self.name = name
        self.compute_via_python = compute_via_python

    def receive(self, callback, message):
        token = parse(message)
        assert token.kind == 'expression'
        calculation = Calculation(token)
        if calculation.action != self.name:
            print str(token)
            print calculation.action
            raise Exception('Wrong bot dispatched.')
        def on_callback(computed_args):
            callback(self.compute_via_python(computed_args))
        calculation.compute_args(on_callback)

class Human:
    def receive(self, callback, message):
        # For now we will do our own computations
        token = parse(message)
        assert token.kind == 'expression'
        calculation = Calculation(token)
        def on_callback(answer):
            print '%s -> %s' % (message, answer)
        send_calculation(on_callback, token)

def send_message(callback, agent, message):
    agent.receive(callback, message)

def send_calculation(callback, token):
    # generalize
    message = str(token)
    action = str(token.tokens[0])
    bot = BOTS[action]
    send_message(callback, bot, message)

BOTS = make_builtin_bots(BuiltinBot)

def run():
    human = Human()
    message = '[ADD [MULT 3 2] [MULT 10 6]]'
    send_message(None, human, message)

if __name__ == '__main__':
    run()
