from bs4 import BeautifulSoup
with open("06_1b.xml") as inputFile:
    soup = BeautifulSoup(inputFile, 'xml')
    sentences = soup.find_all('sentence')
    for sentence in sentences:
        print sentence.text
