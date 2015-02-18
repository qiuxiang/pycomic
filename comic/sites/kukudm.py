# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup
from .base import BaseSite, BaseComic, BaseChapter
from .utils import urlencode


class Site(BaseSite):
    def do_search(self, keyword):
        soup = BeautifulSoup(requests.get(
            'http://so.kukudm.com/search.asp?kw=%s' % urlencode(keyword, 'gbk')).content)
        for item in soup.select('#comicmain dd'):
            anchors = item.find_all('a')
            yield {
                'name': anchors[1].text[:-2],
                'url': anchors[1].get('href'),
                'cover': anchors[0].find('img').get('src'),
            }

    class Comic(BaseComic):
        def fetch_chapters(self):
            soup = BeautifulSoup(requests.get(self.metadata['url']).content)
            self.metadata['description'] = soup.select('#ComicInfo')[0].text
            for item in soup.select('#comiclistn dd'):
                anchor = item.find('a')
                yield {
                    'url': 'http://comic.kukudm.com' + anchor.get('href'),
                    'name': anchor.text,
                }

        class Chapter(BaseChapter):
            def fetch_images(self):
                soup = BeautifulSoup(requests.get(self.metadata['url']).content)
                images = [self.get_image(soup)]
                base_url = self.metadata['url'][:-5]
                for i in range(2, int(re.search(ur'共(\d+)', soup.text).group(1)) + 1):
                    images.append(self.get_image(BeautifulSoup(
                        requests.get('%s%d.htm' % (base_url, i)).content)))
                return images

            def get_image(self, soup):
                return 'http://n.kukudm.com/' + re.search(r'\+\"(.*)\'', soup.text).group(1)
