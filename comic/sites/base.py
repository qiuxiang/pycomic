import os
import requests
from .utils import list_digit


class BaseSite:
    def search(self, keyword):
        results = []
        for item in self.do_search(keyword):
            results.append(self.Comic(item))
        return results


class BaseComic:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_chapters(self):
        if not hasattr(self, 'chapters'):
            self.chapters = []
            for item in self.fetch_chapters():
                self.chapters.append(self.Chapter(item))
        return self.chapters

    def download(self, target):
        directory_template = '%s/%0' + str(list_digit(self.get_chapters())) + 'd'
        for i, item in enumerate(self.get_chapters()):
            directory = directory_template % (target, i + 1)
            if not os.path.isdir(directory):
                os.mkdir(directory)
            item.download(directory)


class BaseChapter:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_images(self):
        if not hasattr(self, 'images'):
            self.images = self.fetch_images()
        return self.images

    def download(self, target):
        directory_template = '%s/%0' + str(list_digit(self.get_images())) + 'd.jpg'
        for i, item in enumerate(self.get_images()):
            filename = directory_template % (target, i + 1)
            if not os.path.isfile(filename):
                open(filename, 'wb').write(requests.get(item, headers={
                    'Referer': self.metadata['url']}).content)
