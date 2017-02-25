import os
# function removes ampersand and replaces misformated

def cleaner(filename):

    # output file name appends a 'b'

    output = filename[:-4] + 'b' + '.xml'
    with open(filename) as xml:
        with open(output, 'w+') as output:
            for line in xml:

                # iterates line by line through the xml and removes ampersands/errors

                line = line.replace('\"id=', 'id=\"')
                line = line.replace('&', '')
                line = line.replace('\n', '')
                output.write(line)


for filename in os.listdir(os.getcwd()): # searches through all files in working directory

    # ignores its own file name

    if filename == 'xmlCleaner.py':
        pass
    else:
        cleaner(filename)
