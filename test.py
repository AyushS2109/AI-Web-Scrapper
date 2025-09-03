import re

def convert_to_dict(st):
    parts = re.split("[:\n]",st)
    dict = {}
    i = 0
    while i < len(parts)-1 : 
        dict[parts[i]] = parts[i+1]
        i += 2
    return dict