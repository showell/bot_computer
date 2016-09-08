import json

def translate(template_source, template_target, args):
    source_params = template_source.split()[1:]
    assert len(source_params) == len(args)
    dct = {source_params[i]: args[i] for i in range(len(args))}
    def _translate(schema):
        if isinstance(schema, list):
            if schema[0] is None:
                return schema[:]
            else:
                return [_translate(item) for item in schema]
        elif isinstance(schema, dict):
            assert len(schema.keys()) == 1
            if schema.keys()[0] == 'name':
                return dct[schema['name']]
            elif schema.keys()[0] == 'value':
                return [None, dct[schema['value']]]
            else:
                raise Exception('unknown type of substitution')
        else:
            return schema

    target_data = _translate(template_target)
    return json.dumps(target_data)


