import os

print(os.getcwd())
try:
    with open('module/file', 'r') as f:
        print('File opened')
except:
    print('Can not open file')

try:
    with open('file', 'r') as f:
        print('Local File opened')
except:
    print('Local Can not open file')
try:
    from module import x
    print('Module imported')
except:
    print('Module not imported')


# os.getcwd()

if __name__ == '__main__':
    pass
