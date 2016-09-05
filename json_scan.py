def scan_token(s):
    i = 0
    while i < len(s):
        if s[i] in '  ]},':
            break
        else:
            i += 1
    return s[:i], s[i:]

def scan_string(s):
    assert s[0] == '"'
    i = 1
    while i < len(s):
        if s[i] == '"':
            return s[:i+1], s[i+1:]
        elif s[0] == '\\':
            i += 2
        else:
            i += 1
    raise Exception('never found end of string')

def scan_list(s):
    assert s[0] == '['
    i = 1
    while True:
        token, rest = scan(s[i:])
        i += len(token)
        print token
        if s[i] == ']':
            return s[:i+1], s[i+1:]
        print s[i:i+2]
        assert s[i:i+2] == ', '
        i += 2

def scan(s):
    if len(s) == 0:
        raise Exception('empty not allowed')

    if s[0] == '"':
        return scan_string(s)
    elif s[0] == '[':
        return scan_list(s)
    else:
        return scan_token(s)

if __name__ == '__main__':
    print scan('"foo" 5')
    print scan('42 rest')
    print scan('42')
    print scan('[5, "7"]foo')
