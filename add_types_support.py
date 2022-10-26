import re
from ast import literal_eval

def is_bin(strng):
    pattern = r"^\s*(?P<bin>[0-1]+)b\s*$"
    match = re.match(pattern,strng)
    if match:
        bin = match.group("bin")
        return bin
    else:
        return False
def is_hex(strng):
    pattern = r"^\s*(?P<hex>0[0-9a-f]+)h\s*$"
    print(type(strng))
    match = re.match(pattern,strng)
    if match:
        hex = match.group("hex")
        return hex
    else:
        return False
def is_oct(strng):
    pattern = r"^\s*(?P<oct>0[0-7]+)[q]\s*$"
    match = re.match(pattern,strng)
    if match:
        oct = match.group("hex")
        return oct
    else:
        return False
def bin_to_dec(strng):
    return str(int(strng,2))

def hex_to_dec(strng):
    return str(int(strng,16))

def oct_to_dec(strng):
    return str(int(strng,8))