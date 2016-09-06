from bot import BOTS
from vm import VirtualMachine
import json

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
