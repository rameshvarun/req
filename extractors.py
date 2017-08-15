from entry import Entry
from bs4 import BeautifulSoup
from mercury_parser.client import MercuryParser
from config import MERCURY_API_KEY

parser = MercuryParser(api_key=MERCURY_API_KEY)

def pdf_extractor(res):
    if res.headers['content-type'] == 'application/pdf':
        return Entry(res.url, 'web/pdf')

def webpage_extractor(res):
    title, summary, url = None, None, res.url

    article = parser.parse_article(res.url)
    if article:
        data = article.json()
        if 'title' in data: title = data['title']
        if 'excerpt' in data: summary = data['excerpt']
        if 'url' in data: url = data['url']

    return Entry(url, 'web', title=title, summary=summary)

extractors = [pdf_extractor, webpage_extractor]
