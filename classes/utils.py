def snake_to_camel(string:str):
    return ''.join(word.title() for word in string.split('_'))