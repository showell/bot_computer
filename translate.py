def translate(template_source, template_target, args):
    source_params = template_source.split()[1:]
    s = template_target
    for i, param in enumerate(source_params):
        s = s.replace(param, args[i])
    return s


