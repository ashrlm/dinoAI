import sys

def parse():
    args = {}
    
    for i in range(len(sys.argv[1:])):
        if sys.argv[i][0] == '-':
            args[sys.argv[i].replace('-', '')] = sys.argv[i+1]
    
    return args
    
print(parse())