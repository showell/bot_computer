import json

class ExpressionToken:
    def __init__(self, val):
        self.kind = 'expression'
        self.full_val = val
        self.action = val[0]
        self.args = [make_arg(val) for val in val[1:]]

    def __str__(self):
        return json.dumps(self.full_val)

class LiteralToken:
    def __init__(self, val):
        self.kind = 'literal'
        self.full_val = val
        self.val = val[1]

def make_arg(val):
    if val[0]:
        return ExpressionToken(val)
    else:
        return LiteralToken(val)

def parse(s):
    val = json.loads(s)
    return ExpressionToken(val)

if __name__ == '__main__':
    print tokenize('(ADD)')
