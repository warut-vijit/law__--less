import os
from bs4 import BeautifulSoup
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# function removes ampersand and replaces misformated data.
# outputs end as text

def pdf2text(fname, pages = None):
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

def cleaner(text, filename):

    # output file name appends a 'b'

    output = filename[:-4] + '.txt'

    with open(output, 'w+') as output:
        for line in text:

            # iterates line by line through the text and removes ampersands/errors

            line = line.replace('\"id=', 'id=\"')
            line = line.replace('&', '')
            line = line.replace('\n', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.replace('\'', '')
            line = line.replace('\"', '')
            line = line.replace('{', '')
            line = line.replace('}', '')

            output.write(line)


for filename in os.listdir(os.getcwd()): # searches through all files in working directory

    # only uses .pdf file

    if filename[-4:] != '.pdf':
        pass
    else:
        cleaner(pdf2text(filename), filename)

for filename in os.listdir(os.getcwd()): # searches through all files in working directory

    if filename[-4:] == '.pdf':
        os.remove(filename)
