from json_scan import scan

def scan_token(s):
    i = 0
    while i < len(s):
        if s[i] in ' \n)':
            break
        else:
            i += 1
    return s[:i]

def len_ws(s):
    i = 0
    while i < len(s):
        if s[i] in ' \n':
            i += 1
        else:
            break
    return i

def tokenize(s):
    res = []
    i = 0
    t = ''
    i = 0
    while i < len(s):
        i += len_ws(s[i:])
        c = s[i]
        if c == '(':
            res.append(c)
            i += 1
            i += len_ws(s[i:])
            new_token = scan_token(s[i:])
            res.append(new_token)
            i += len(new_token)
        elif c == ')':
            res.append(c)
            i += 1
        else:
            token = scan(s[i:])
            res.append(token)
            i += len(token)
    return res

class LiteralToken:
    def __init__(self, val):
        self.val = val
        self.kind = 'literal'

    def __str__(self):
        return self.val

class ExpressionToken:
    def __init__(self, tokens):
        self.tokens = tokens
        self.kind = 'expression'

    def __str__(self):
        return '(' + ' '.join(str(t) for t in self.tokens) + ')'

def parse(s):
    tokens = tokenize(s)

    def _parse_bracket_expr(tokens):
        tokens = tokens[1:]
        res = []
        while True:
            if not tokens:
                raise Exception('unclosed bracket')
            if tokens[0] == ')':
                return ExpressionToken(res), tokens[1:]
            else:
                head, rest = _parse(tokens)
                assert head
                res.append(head)
                tokens = rest

    def _parse(tokens):
        if not tokens:
            return None, None
        if tokens[0] == '(':
            return _parse_bracket_expr(tokens)
        else:
            return LiteralToken(tokens[0]), tokens[1:]


    lst, rest = _parse(tokens)
    assert rest == []
    return lst

if __name__ == '__main__':
    print tokenize('(ADD)')
