import os
import string
from bs4 import BeautifulSoup

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

def xmlToText(filename):

    # convert xml input to .txt output

    with open(filename[:-4] + 'b' + '.xml') as inputFile:
        with open(filename[:-4] + '.txt', 'w+') as output:
            soup = BeautifulSoup(inputFile, 'lxml')
            sentences = soup.find_all('sentence')
            #print(sentences[0])
            for sentence in sentences:
                #print(sentence)
                output.write(sentence.text)

def cleanText(filename):

    filename = filename[:-4] + '.txt'
    output = filename[:-4] + 'b' + '.txt'
    with open(filename) as file:
        with open(output, 'w+') as textFile:
            for line in file:
                line = line.replace('[', '')
                line = line.replace(']', '')
                line = line.replace("\'", '')
                line = line.replace('\"', '')
                line = line.replace('<','')
                line = line.replace('>','')
                textFile.write(line)
    os.remove(filename)
    os.rename(output, filename)


for filename in os.listdir(os.getcwd()): # searches through all files in working directory

    # only uses .xml file

    if filename[-4:] != '.xml':
        pass
    else:
        cleaner(filename)
        xmlToText(filename)
        cleanText(filename)

for filename in os.listdir(os.getcwd()): # searches through all files in working directory

    if filename[-5:] == 'b.xml':
        os.remove(filename)
