import json

def parse(s):
    try:
        val = json.loads(s)
    except:
        raise Exception('illegal json: %s' % s)
    return val

if __name__ == '__main__':
    print tokenize('(ADD)')
