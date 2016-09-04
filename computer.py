from parser import parse
from builtin import make_builtin_bots
from calculate import Calculation, make_arg
from translate import translate

class BuiltinBot:
    def __init__(self, name, compute_via_python):
        self.name = name
        self.compute_via_python = compute_via_python

    def receive(self, callback, message):
        token = parse(message)
        assert token.kind == 'expression'
        calculation = Calculation(token, send_calculation)
        if calculation.action != self.name:
            print str(token)
            print calculation.action
            raise Exception('Wrong bot dispatched.')
        def on_callback(computed_args):
            callback(self.compute_via_python(computed_args))
        calculation.compute_args(on_callback)

class Human:
    def receive(self, callback, message):
        token = parse(message)
        assert token.kind == 'expression'
        calculation = Calculation(token, send_calculation)
        def on_callback(answer):
            print '%s -> %s' % (message, answer)
        send_calculation(on_callback, token)

class IfBot:
    def receive(self, callback, message):
        token = parse(message)
        calculation = Calculation(token.tokens[1], send_calculation)
        def on_callback(answer):
            if answer:
                make_arg(token.tokens[2], send_calculation).compute(callback)
            else:
                make_arg(token.tokens[3], send_calculation).compute(callback)
        calculation.compute(on_callback)

class TranslateBot:
    def __init__(self, template_source, template_target):
        self.template_source = template_source
        self.template_target = template_target

    def receive(self, callback, message):
        token = parse(message)
        calculation = Calculation(token, send_calculation)
        calculation.compute_args(
            lambda args: self.compute(callback, args))

    def compute(self, callback, computed_args):
        args = [str(ca) for ca in computed_args]
        new_message = '(' + translate(
            template_source=self.template_source,
            template_target=self.template_target,
            args=args) + ')'
        token = parse(new_message)
        assert token.kind == 'expression'
        calculation = Calculation(token, send_calculation)
        send_calculation(callback, token)

def send_message(callback, agent, message):
    agent.receive(callback, message)

def send_calculation(callback, token):
    # generalize
    message = str(token)
    action = str(token.tokens[0])
    bot = BOTS[action]
    send_message(callback, bot, message)

BOTS = make_builtin_bots(BuiltinBot)

BOTS['SQUARE'] = TranslateBot(
    template_source='SQUARE x',
    template_target='MULT x x'
)
BOTS['FACTORIAL'] = TranslateBot(
    template_source='FACTORIAL x',
    template_target='IF (EQ x 0) 1 (MULT x (FACTORIAL (ADD x -1)))'
)
BOTS['IF'] = IfBot()

def run():
    human = Human()
    message = '(FACTORIAL 5)'
    send_message(None, human, message)

if __name__ == '__main__':
    run()
