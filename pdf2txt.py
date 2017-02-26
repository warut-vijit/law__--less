import os
from bs4 import BeautifulSoup
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# function removes ampersand and replaces misformated data.
# outputs end as xml

def convert(fname, pages = None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

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
                line = line.replace('[', '')
                line = line.replace(']', '')
                line = line.replace('\'', '')
                line = line.replace('\"', '')

                output.write(line)

def xmlToText(filename):

    # convert xml input to .txt output

    with open(filename) as inputFile:
        with open(filename[:-4] + '.txt', 'w+') as output:
            soup = BeautifulSoup(inputFile, 'xml')
            sentences = soup.find_all('sentence')
            for sentence in sentences:
                output.write(sentence.text)


for filename in os.listdir(os.getcwd()): # searches through all files in working directory

    # only uses .xml file

    if filename[-4:] != '.xml':
        pass
    else:
        cleaner(filename)
        xmlToText(filename)

for filename in os.listdir(os.getcwd()): # searches through all files in working directory

    if filename[-4:] == '.xml':
        print('deleting')
        os.remove(filename)
