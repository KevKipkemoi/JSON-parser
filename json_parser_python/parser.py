from .constants import *

def parse_array(tokens):
    json_array = []
    token = tokens[0]

    if token == JSON_RIGHTBRACKET:
        return json_array, tokens[1:]

    while True:
        json, tokens = parse(tokens)
        json_array.append(json)
        token = tokens[0]
        if token == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]
        elif token != JSON_COMMA:
            raise Exception('Expected comma after array object')
        else:
            tokens = tokens[1:]
        raise Exception('Expected end-of-array object')

def parse_object(tokens):
    json_object = {}
    token = tokens[1:]
    if token == JSON_RIGHTBRACKET:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception('Expected string key, got: {}'.format(json_key))

        if tokens[0] != JSON_COLON:
            raise Exception('Expected colon after key in object, got: {}'.format(token))

        json_value, tokens = parse(tokens[1:])
        json_object[json_key] = json_value
        token = tokens[0]

        if token == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
        elif token != JSON_COMMA:
            raise Exception('Expected comma after pair object, got: {}'.format(token))
        tokens = tokens[1:]

    raise Exception('Expected end-of-object bracket')

def parse(tokens, is_root = False):
    token = tokens[0]
    if is_root and token != JSON_LEFTBRACE:
        raise Exception('Root must be an object')

    if token == JSON_LEFTBRACKET:
        return parse_array(tokens[1:])
    elif token == JSON_LEFTBRACE:
        return parse_object(tokens[1:])
    else:
        return token, tokens[1:]
