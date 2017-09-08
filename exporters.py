import click
from entry import get_entries
from urlifiers import urlify
import requests
import sys
from slugify import slugify
import time

@click.command('pinboard')
@click.option('--auth-token', required=True)
def pinboard(auth_token):
    """Export saved entries into Pinboard"""


    existing_links = requests.get('https://api.pinboard.in/v1/posts/all', params={
        'auth_token': auth_token,
        'format': 'json',
    }).json()
    existing_links = set(link['href'] for link in existing_links)

    entries = get_entries()
    unsynced_entries = [e for e in entries if urlify(e) not in existing_links]

    print(f"{len(unsynced_entries)} entries to sync...")

    def show_item(entry):
        if entry == None:
            return ""
        return (entry.title or urlify(entry))[:50]

    with click.progressbar(unsynced_entries, item_show_func=show_item, label='Exporting to Pinboard...') as bar:
        for entry in bar:
            url = urlify(entry)
            title = entry.title or url

            time.sleep(3)

            res = requests.get('https://api.pinboard.in/v1/posts/add', params={
                'auth_token': auth_token,
                'url': url,
                'description': title,
                'extended': entry.summary,
                'toread': 'no' if entry.read else 'yes',
                'replace': 'no',
                'dt': entry.time_added.isoformat(),
                'tags': [slugify(tag) for tag in entry.tags],
                'format': 'json',
            })

            result_code = res.json()['result_code']
            if result_code != 'done' and result_code != 'item already exists':
                click.echo(f"Failed to add {title} with result code '{result_code}'.", err=True)

@click.group()
def export(): pass
export.add_command(pinboard)
