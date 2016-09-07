import json

def translate(template_source, template_target, args):
    source_params = template_source.split()[1:]
    assert len(source_params) == len(args)
    s = template_target
    for i, param in enumerate(source_params):
        arg = args[i]
        s = s.replace(param, arg)
    return s


