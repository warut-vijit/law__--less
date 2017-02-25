import os

# function removes ampersand and replaces misformated

def cleaner(filename):

    # output file name appends a 'b'

    output = filename[:-4] + 'b' + '.xml'
    with open(filename) as xml:
        with open(output, 'a+') as output:
            for line in xml:

                # iterates line by line through the xml and removes ampersands/errors

                line = line.replace('\"id=', 'id=\"')
                line = line.replace('&', '')
                output.write(line)


fileDir = input("Input path to files to be cleaned: ")
for filename in os.listdir(fileDir):

    # ignores its own file

    if filename == 'xmlCleaner.py':
        pass
    else:
        cleaner(filename)
