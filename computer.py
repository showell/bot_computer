from parser import parse
from builtin import make_builtin_bots
from calculate import Calculation
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

class TranslateBot:
    def __init__(self, template_source, template_target):
        self.template_source = template_source
        self.template_target = template_target

    def receive(self, callback, message):
        token = parse(message)
        args = [str(t) for t in token.tokens[1:]]
        new_message = '[' + translate(
            template_source=self.template_source,
            template_target=self.template_target,
            args=args) + ']'
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


def run():
    human = Human()
    message = '[ADD [IF 0 5 3] [MULT 10 7]]'
    send_message(None, human, message)

if __name__ == '__main__':
    run()
