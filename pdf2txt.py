import os
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# function removes ampersand and replaces misformated data.
# outputs end as text

def pdf2text(fobject, pages = None):

    # converts pdf files to text using pdfminer

    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    #infile = file(fname, 'rb')
    infile = fobject
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def cleaner(text):
    out_text = ""
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
        line = line.replace('(', '')
        line = line.replace(')', '')
        out_text += ''.join(i for i in line if ord(i) < 128)
    return out_text

# used as cleaner(pdf2text(file object), name)
# returns long filtered string
