from bs4 import BeautifulSoup
import os

def textMaker(filename):
    with open(filename) as inputFile:
        with open(filename[:-4] + '.txt', 'w+') as output:
            soup = BeautifulSoup(inputFile, 'xml')
            sentences = soup.find_all('sentence')
            for sentence in sentences:
                output.write(sentence.text)


for filename in os.listdir(os.getcwd()):
    if filename[-4:] != '.xml':
        pass
    else:
        textMaker(filename)
