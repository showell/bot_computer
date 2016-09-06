from bot import BOTS, Human
import json


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
    def send(cnt):
        def my_callback(answer):
            REQUESTS[cnt] = message
            CALLBACKS[cnt] = callback
            REPLIES.append((cnt, answer))
        MESSAGES.append((agent, my_callback, message))
    send(CNT)
    CNT += 1

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
            agent.receive(send_calculation, my_callback, message)

def send_calculation(callback, token):
    # generalize
    message = str(token)
    action = str(token.tokens[0])
    bot = BOTS[action]
    send_message(callback, bot, message)

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
        '(MATH_TABLE 7)',
    ]
    for message in messages:
        if VERBOSE:
            print "\n\n--"
        reset_event_loop()

        def callback(answer):
            print '%s -> %s' % (message, repr(answer))

        send_message(callback, human, message)
        event_loop()

if __name__ == '__main__':
    run()
