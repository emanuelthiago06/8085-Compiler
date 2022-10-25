import re
import values


comments = [] # Implementar os comentários no futuro 
#txt = 'ADD C'
patterns = [
    r'^\s*(?P<command>[\w]+)\s*(?:;[\w\W\s]*)?$',
    r'^\s*(?P<command>\w+)\s*(?P<arg1>\w+)\s*(?:;[\w\s\W]*)?$', # ADD C
    r'^\s*(?P<command>\w+)\s+(?P<arg1>\w+)\s*,\s*(?P<arg2>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>[a-z]\w*):\s*(?P<command>\w+)\s+(?P<arg1>\w+)\s*,\s*(?P<arg2>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>[a-z]\w*):\s*(?P<command>\w+)\s+(?P<arg1>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>[a-z]\w*):\s*(?P<command>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>[a-z]\w*):\s*(?:;[\w\s\W]*)?$'
]
#match = re.search('(?P<name>.*) (?P<phone>.*)', 'John 123456')
#print(match)
#pattern = re.compile(patterns[0])
#match = re.search(patterns[0],txt)
#print(pattern.findall(txt))
#print(match.group('arg2'))
