import json

def translate(template_source, template_target, args):
    source_params = template_source.split()[1:]
    assert len(source_params) == len(args)
    dct = {source_params[i]: args[i] for i in range(len(args))}
    def _translate(schema):
        if isinstance(schema, list):
            if schema[0] == 'data':
                return schema[:]
            else:
                return [_translate(item) for item in schema]
        elif isinstance(schema, dict):
            assert len(schema.keys()) == 1
            if schema.keys()[0] == 'value':
                return ["data", dct[schema['value']]]
            else:
                raise Exception('unknown type of substitution')
        else:
            return schema

    target_data = _translate(template_target)
    return target_data

def indent(text, num_spaces):
    def indent_line(line):
        if line == '':
            return ''
        else:
            return (' ' * num_spaces) + line

    lines = text.split('\n')
    lines = [indent_line(line) for line in lines]
    return '\n'.join(lines)

def translate_to_python(commands):
    def translate_expression(expr):
        if type(expr) is dict:
            return expr['value']

        func_name = expr[0]
        if type(func_name) is dict:
            func_name = func_name['value']

        if func_name == 'apply':
            func_name = 'globals()[%s]' % translate_expression(expr[1][0])
            args = expr[1][1:]
            return translate_expression([func_name] + args)

        if func_name == 'data':
            val = expr[1]
            if type(val) is dict:
                val = val['value']
            else:
                val = repr(val)
            return val

        args = [translate_expression(arg) for arg in expr[1:]]

        if func_name == 'deref':
            return '%s[%s]' % (args[1], args[0])

        if func_name == 'if':
            code = '(\n%s\nif\n%s\nelse\n%s)' % (
                indent(args[1], 4),
                indent(args[0], 4),
                indent(args[2], 4))
            return code

        if func_name == 'eq':
            return '%s == %s' % (args[0], args[1])

        if func_name == 'list':
            code = ',\n'.join(args)
            return '[' + code + ']'

        if func_name == 'add':
            code = ' + \n'.join(args)
            return '(' + code + ')'

        if func_name == 'multiply':
            code = ' * \n'.join(args)
            return '(' + code + ')'

        # start normal case here
        code = ''
        code += '%s(\n' % func_name
        for i, arg in enumerate(args):
            s = arg
            if (i + 1) < len(args):
                s += ',\n'
            code += indent(s, 4)
        code += ')'

        return code

    def translate_body(body):
        code = 'return \\\n'
        code += indent(translate_expression(body), 4)
        return indent(code, 4)

    program = ''
    for command in commands:
        param_def, body = command
        tokens = param_def.split()
        func_name = tokens[0]
        params = tokens[1:]
        program += 'def %s(%s):\n' % (func_name, ', '.join(params))
        program += translate_body(body)
        program += '\n\n'

    return program


if __name__ == '__main__':
    from commands import COMMANDS
    code = translate_to_python(COMMANDS)
    code += '''
print math_table(range(5, 15))
'''
    fn = '/tmp/foo.py'
    open(fn, 'w').write(code)
    import subprocess
    subprocess.call(['python', fn])


