def tokenize(s):
    res = []
    i = 0
    t = ''
    for i, c in enumerate(s):
        if c in '[] ':
            if t:
                res.append(t)
            if c != ' ':
                res.append(c)
            t = ''
        else:
            t += c
    if t:
        res.append(t)
    return res

class LiteralToken:
    def __init__(self, s):
        self.s = s
        self.kind = 'literal'

    def __str__(self):
        return self.s

class ExpressionToken:
    def __init__(self, tokens):
        self.tokens = tokens
        self.kind = 'expression'

    def __str__(self):
        return '[' + ' '.join(str(t) for t in self.tokens) + ']'

def parse(s):
    tokens = tokenize(s)

    def _parse_bracket_expr(tokens):
        tokens = tokens[1:]
        res = []
        while True:
            if not tokens:
                raise Exception('unclosed bracket')
            if tokens[0] == ']':
                return ExpressionToken(res), tokens[1:]
            else:
                head, rest = _parse(tokens)
                assert head
                res.append(head)
                tokens = rest

    def _parse(tokens):
        if not tokens:
            return None, None
        if tokens[0] == '[':
            return _parse_bracket_expr(tokens)
        else:
            return LiteralToken(tokens[0]), tokens[1:]


    lst, rest = _parse(tokens)
    assert rest == []
    return lst

