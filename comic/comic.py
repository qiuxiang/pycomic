# coding: utf-8


def load_site(classname):
    return getattr(__import__('sites.' + classname), classname)


if __name__ == '__main__':
    comic = load_site('dmzj')
    print comic.search('妖精')
