# coding: utf-8


def load_site(classname):
    return getattr(__import__('sites.' + classname), classname).Site()


if __name__ == '__main__':
    comic = load_site('dmzj')
    print(comic.search('妖精')[1].get_chapters()[0].get_images())
