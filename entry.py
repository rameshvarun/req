import secrets
import yaml

from typing import *
from datetime import datetime

import dateutil.parser

from config import DATA_FOLDER
from collections import OrderedDict

class Entry:
    def __init__(self,
            resource_id: str,
            resource_type: str,

            handle: Optional[str] = None,

            title: Optional[str] = None,
            summary: str = "",

            read: bool = False,

            time_added = None,

            notes: str = "",
            tags: List[str] = []) -> None:

        self.resource_id = resource_id
        self.resource_type = resource_type

        self.handle = handle or secrets.token_hex(3)

        self.title = title
        self.summary = summary

        self.read = read

        self.time_added = time_added or datetime.now()

        self.notes = notes
        self.tags = list(tags)

    def __repr__(self):
        return f"{self.handle}:{self.resource_type}:{self.resource_id}"

    def save(self):
        with open(DATA_FOLDER / f"{self.handle}.yml", "w") as f:
            f.write(yaml.dump({
                'read': self.read,
                'resource_id': self.resource_id,
                'resource_type': self.resource_type,
                'title': self.title,
                'summary': self.summary,
                'time_added': self.time_added.isoformat(),
                'tags': self.tags,
                'notes': self.notes,
            }))

def load_entry(file_path):
    with open(file_path, 'r') as f:
        data = yaml.load(f.read())
        return Entry(
            data['resource_id'],
            data['resource_type'],
            file_path.stem,
            data['title'],
            data['summary'],
            data['read'],
            dateutil.parser.parse(data['time_added']),
            data['notes'],
            data['tags'])

def get_entries():
    paths = [f for f in DATA_FOLDER.iterdir() if f.suffix == '.yml']
    entries = [load_entry(p) for p in paths]
    return entries
