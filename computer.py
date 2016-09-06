from bot import BOTS
import json

VERBOSE = False

class VirtualMachine:
    def __init__(self, bots):
        self.cnt = 0
        self.bots = bots
        self.requests = {}
        self.callbacks = {}
        self.messages = []
        self.replies = []

    def send_message(self, callback, agent, message):
        def send(cnt):
            def my_callback(answer):
                self.requests[cnt] = message
                self.callbacks[cnt] = callback
                self.replies.append((cnt, answer))
            self.messages.append((agent, my_callback, message))
        send(self.cnt)
        self.cnt += 1

    def event_loop(self):
        while self.messages or self.replies:
            while self.replies:
                cnt, answer = self.replies.pop(0)
                self.callbacks[cnt](answer)
                if VERBOSE:
                    print '  %4d: %s -> %s' % (
                        cnt,
                        self.requests[cnt],
                        json.dumps(answer))
                del self.callbacks[cnt]
                del self.requests[cnt]
            while self.messages:
                agent, my_callback, message = self.messages.pop(0)
                agent.receive(self.send_calculation, my_callback, message)

    def send_calculation(self, callback, token):
        # generalize
        message = str(token)
        action = str(token.tokens[0])
        bot = self.bots[action]
        self.send_message(callback, bot, message)

    def process_message(self, message):
        human = self.bots['Human']
        if VERBOSE:
            print "\n\n--"

        def callback(answer):
            print '%s -> %s' % (message, repr(answer))

        self.send_message(callback, human, message)
        self.event_loop()

def run():
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
        '(MATH_TABLE 7)',
    ]
    for message in messages:
        vm = VirtualMachine(BOTS)
        vm.process_message(message)


if __name__ == '__main__':
    run()
