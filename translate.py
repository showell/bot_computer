import json

def translate(template_source, template_target, args):
    source_params = template_source.split()[1:]
    s = template_target
    for i, param in enumerate(source_params):
        arg = args[i]
        s = s.replace(':' + param, str(json.loads(arg)))
        if ('*' + param) in s:
            splatted_arg = ' '.join(json.dumps(a) for a in json.loads(arg))
            s = s.replace('*' + param, splatted_arg)
        s = s.replace(param, arg)
    splat_args = args[len(source_params):]
    s = s.replace('...', ' '.join(splat_args))
    return s


