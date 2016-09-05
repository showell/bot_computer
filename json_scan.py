def scan_token(s):
    i = 0
    while i < len(s):
        if s[i] in '  ]}),':
            break
        else:
            i += 1
    if i == 0:
        print 'scan_token', s
        raise Exception('could not find token')
    return s[:i]

def scan_string(s):
    assert s[0] == '"'
    i = 1
    while i < len(s):
        if s[i] == '"':
            return s[:i+1]
        elif s[0] == '\\':
            i += 2
        else:
            i += 1
    raise Exception('never found end of string')

def ws(s):
    i = 0
    while i < len(s) and s[i] in ' \n':
        i += 1
    return i

def scan_list(s):
    assert s[0] == '['
    if s[1] == ']':
        return s[:2]
    i = 1
    i += len(scan(s[i:]))
    while True:
        if s[i] == ']':
            return s[:i+1]
        assert s[i] == ','
        i += 1
        i += ws(s[i:])
        i += len(scan(s[i:]))

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
