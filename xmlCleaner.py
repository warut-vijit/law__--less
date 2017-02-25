import os

def cleaner(filename):
    output = filename[:-4] + 'b' + '.xml'
    with open(filename) as xml:
        with open(output, 'a+') as output:
            for line in xml:
                line = line.replace('\"id=', 'id=\"')
                line = line.replace('&', '')
                output.write(line)


for filename in os.listdir("C:/Users/naveed/Documents/fulltext"):
    if filename == 'textScript.py':
        pass
    else:
        cleaner(filename)
