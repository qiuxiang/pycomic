import json
import re
import requests
import execjs
from bs4 import BeautifulSoup
from .base import BaseSite, BaseComic, BaseChapter


class Site(BaseSite):
    def search(self, keyword):
        results = []
        for item in json.loads(requests.get(
                'http://s.acg.178.com/comicsum/search.php?s=' + keyword).text[20:-1]):
            if item['hidden'] == '0':
                results.append(Comic({
                    'description': item['description'],
                    'url': item['comic_url'],
                    'author': item['authors'],
                    'cover': item['cover'],
                    'name': item['name'],
                }))
        return results


class Comic(BaseComic):
    def get_chapters(self):
        results = []
        soup = BeautifulSoup(requests.get(self.metadata['url']).text)
        for item in soup.select('.cartoon_online_border a'):
            results.append(Chapter({
                'url': 'http://manhua.dmzj.com' + item.get('href'),
                'name': item.text,
            }))
        return results


class Chapter(BaseChapter):
    def get_images(self):
        return ['http://images.dmzj.com/' + item for item in json.loads(execjs.exec_(re.search(
            r'(eval.*\))', requests.get(self.metadata['url']).text).group(1) + ';return pages'))]
