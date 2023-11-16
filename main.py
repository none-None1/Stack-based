from stackbased import stack_based
import sys

if len(sys.argv) == 1:
    stack_based(sys.stdin.read())
else:
    f = open(sys.argv[1])
    try:
        stack_based(f.read())
    except:
        pass
    f.close()
