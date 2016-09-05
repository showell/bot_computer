from parser import parse
from builtin import make_builtin_bots
from calculate import Calculation, make_arg
from translate import translate
from commands import COMMANDS
import json

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
            print '%s -> %s' % (message, repr(answer))
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
        args = [json.dumps(ca) for ca in computed_args]
        new_message = '(' + translate(
            template_source=self.template_source,
            template_target=self.template_target,
            args=args) + ')'
        token = parse(new_message)
        assert token.kind == 'expression'
        calculation = Calculation(token, send_calculation)
        send_calculation(callback, token)

VERBOSE = False
CNT = 0
CALLBACKS = {}
REQUESTS = {}
MESSAGES = []
REPLIES = []

def reset_event_loop():
    global CNT
    CNT = 0
    assert REQUESTS == {}
    assert MESSAGES == []
    assert REPLIES == []

def send_message(callback, agent, message):
    global CNT
    CNT += 1
    def send(cnt):
        def my_callback(answer):
            REQUESTS[cnt] = message
            CALLBACKS[cnt] = callback
            REPLIES.append((cnt, answer))
        MESSAGES.append((agent, my_callback, message))
    send(CNT)

def event_loop():
    while MESSAGES or REPLIES:
        while REPLIES:
            cnt, answer = REPLIES.pop(0)
            CALLBACKS[cnt](answer)
            if VERBOSE:
                print '  %4d: %s -> %s' % (cnt, REQUESTS[cnt], json.dumps(answer))
            del CALLBACKS[cnt]
            del REQUESTS[cnt]
        while MESSAGES:
            agent, my_callback, message = MESSAGES.pop(0)
            agent.receive(my_callback, message)

def send_calculation(callback, token):
    # generalize
    message = str(token)
    action = str(token.tokens[0])
    bot = BOTS[action]
    send_message(callback, bot, message)

BOTS = make_builtin_bots(BuiltinBot)

for source, target in COMMANDS:
    name = source.split()[0]
    BOTS[name] = TranslateBot(template_source=source, template_target=target)

BOTS['IF'] = IfBot()

def run():
    human = Human()
    messages = [
        '(FACTORIAL 5)',
        '(ADD [1, 2] [3, 4])',
        '(SQUARE 7)',
        '(DOUBLE 13)',
        '(TAG "td" "some value")',
        '(RANGE 5 15)',
        '(APPLY "ADD" (ADD 4 5) 10)',
        '(APPLY "ADD" (ADD "x" "y") "z")',
        '(DEREF 2 ["apple", "banana", "carrot", "dog"])',
        '(MAP_ONE 0 [1, 2] "DOUBLE")',
        '(LEN [0, 1, 2, 3, 4])',
        '(LIST 5 7 9)',
        '(MAP_REST 0 [1, 2, 3] "DOUBLE")',
        '(MAP [1, 2, 3] "SQUARE")',
        '(SPLAT "ADD" [1, 2, 3])',
        '(MATH_ROW 7)',
        '(MATH_TR 7)',
    ]
    for message in messages:
        if VERBOSE:
            print "\n\n--"
        reset_event_loop()
        send_message(None, human, message)
        event_loop()

if __name__ == '__main__':
    run()
