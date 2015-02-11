import requests
import json
from bs4 import BeautifulSoup


def search(keyword):
    results = []
    for item in json.loads(requests.get('http://s.acg.178.com/comicsum/search.php?s=' + keyword).content[20:-1]):
        results.append(comic({
            'description': item['description'],
            'url': item['comic_url'],
            'author': item['authors'],
            'cover': item['cover'],
            'name': item['name'],
        }))
    return results


def comic(metadata):
    return metadata
