import json
from builtin import make_builtin_bots
from commands import COMMANDS
from parser import parse
from calculate import Calculation, make_arg
from translate import translate

class BuiltinBot:
    def __init__(self, name, compute_via_python):
        self.name = name
        self.compute_via_python = compute_via_python

    def receive(self, send_calculation, callback, message):
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

class DispatchBot:
    '''
    The dispatch bot really does nothing but call back into the
    VM.  It's questionable really it clarifies anything to have
    this as kind of the "root" of the calculation.  This could be
    more like the "human" who is asking all the other bots to do
    work for it.
    '''
    def receive(self, send_calculation, callback, message):
        token = parse(message)
        assert token.kind == 'expression'
        send_calculation(callback, token.action, message)

class IfBot:
    def receive(self, send_calculation, callback, message):
        token = parse(message)
        calculation = make_arg(token.args[0], send_calculation)
        def on_callback(answer):
            if answer:
                make_arg(token.args[1], send_calculation).compute(callback)
            else:
                make_arg(token.args[2], send_calculation).compute(callback)
        calculation.compute(on_callback)

class TranslateBot:
    def __init__(self, template_source, template_target):
        self.template_source = template_source
        self.template_target = template_target

    def receive(self, send_calculation, callback, message):
        token = parse(message)
        calculation = Calculation(token, send_calculation)
        calculation.compute_args(
            lambda args: self.compute(send_calculation, callback, args))

    def compute(self, send_calculation, callback, computed_args):
        args = [json.dumps(ca) for ca in computed_args]
        new_message = translate(
            template_source=self.template_source,
            template_target=self.template_target,
            args=args)
        token = parse(new_message)
        assert token.kind == 'expression'
        send_calculation(callback, token.action, new_message)

BOTS = make_builtin_bots(BuiltinBot)

for source, target in COMMANDS:
    name = source.split()[0]
    BOTS[name] = TranslateBot(template_source=source, template_target=target)

BOTS['IF'] = IfBot()

BOTS['Dispatch'] = DispatchBot()

