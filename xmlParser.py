from bs4 import BeautifulSoup

soup = BeautifulSoup("clean.xml", 'xml')
sentences = soup.find_all('sentece')
for sentence in senteces:
    print sentece.text
