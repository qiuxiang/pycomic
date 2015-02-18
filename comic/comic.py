# coding: utf-8
def load_site(classname):
    return getattr(__import__('sites.' + classname), classname).Site()


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    comic = load_site('kukudm')
    print(comic.search('妖精')[0].get_chapters()[0].get_images())
