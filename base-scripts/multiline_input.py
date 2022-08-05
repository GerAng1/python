"""Allows for user to paste multi-line text without breaking
until user inputs EOF (with CTR-D/Mac or CTR-Z/Windows)
"""

while True:
    filename = input("Your Filename: ")

    contents = []
    print('Contents (end with CTR-D or CTR-Z on an empty line):')

    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    with open(filename + '.txt', 'w') as f:
        for line in contents:
            f.write(line + '\n')
