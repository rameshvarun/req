import click

from enum import Enum, auto
from html.parser import HTMLParser
from collections import namedtuple

from entry import Entry

from datetime import datetime

@click.command('pocket-import')
@click.argument('file', type=click.File('rb'))
def pocket_import(file):
    """Import your reading list from Pocket's exported HTML."""

    class PocketParserState(Enum):
        INITIAL = auto()

        UNREAD_LIST = auto()
        UNREAD_LINK = auto()

        READ_LIST = auto()
        READ_LINK = auto()

    Tag = namedtuple('Tag', ['name', 'attrs'])
    PocketResult = namedtuple('PocketResult', ['title', 'url', 'read', 'tags', 'time_added'])

    pocket_results = []

    class PocketHTMLParser(HTMLParser):
        def __init__(self):
            self.state = PocketParserState.INITIAL
            self.tag_stack = []
            super().__init__()

        def handle_starttag(self, tag, attrs):
            self.tag_stack.append(Tag(tag, dict(attrs)))
            if self.state == PocketParserState.INITIAL:
                if tag == 'ul': self.state = PocketParserState.UNREAD_LIST
            elif self.state == PocketParserState.UNREAD_LIST:
                if tag == 'a': self.state = PocketParserState.UNREAD_LINK
                elif tag == 'ul': self.state = PocketParserState.READ_LIST
            elif self.state == PocketParserState.READ_LIST:
                if tag == 'a': self.state = PocketParserState.READ_LINK

        def handle_endtag(self, tag):
            self.tag_stack.pop()
            if self.state == PocketParserState.UNREAD_LINK:
                if tag == 'a': self.state = PocketParserState.UNREAD_LIST
            elif self.state == PocketParserState.READ_LINK:
                if tag == 'a': self.state = PocketParserState.READ_LIST

        def handle_data(self, data):
            if self.state == PocketParserState.UNREAD_LINK or self.state == PocketParserState.READ_LINK:
                a_tag = self.tag_stack[-1]

                read = self.state == PocketParserState.READ_LINK
                time_added = datetime.utcfromtimestamp(int(a_tag.attrs['time_added']))
                tags = a_tag.attrs['tags'].split(",")
                url = a_tag.attrs['href']

                pocket_results.append(PocketResult(data, url, read, tags, time_added))

    parser = PocketHTMLParser()
    parser.feed(file.read().decode())

    for pr in pocket_results:
        entry = Entry(pr.url, 'web', title=pr.title, tags=pr.tags,
            read=pr.read, time_added=pr.time_added)
        entry.save()
