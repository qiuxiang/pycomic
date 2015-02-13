import json
import re
import requests
import execjs
from bs4 import BeautifulSoup


class Site:
    def search(self, keyword):
        results = []
        for item in json.loads(requests.get('http://s.acg.178.com/comicsum/search.php?s=' + keyword).content[20:-1]):
            if item['hidden'] == '0':
                results.append(Comic({
                    'description': item['description'],
                    'url': item['comic_url'],
                    'author': item['authors'],
                    'cover': item['cover'],
                    'name': item['name'],
                }))
        return results


class Comic:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_chapters(self):
        results = []
        soup = BeautifulSoup(requests.get(self.metadata['url']).content)
        for item in soup.select('.cartoon_online_border a'):
            results.append(Chapter({
                'url': 'http://manhua.dmzj.com' + item.get('href'),
                'name': item.text,
            }))
        return results


class Chapter:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_images(self):
        return ['http://images.dmzj.com/' + item for item in json.loads(execjs.exec_(re.search(
            r'(eval.*\))', requests.get(self.metadata['url']).content).group(1) + ';return pages'))]
