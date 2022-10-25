import sys
from compiler import Comp8085

comp = Comp8085(sys.argv[1])
comp.runner()