import urllib


def list_digit(_list):
    return len(str(len(_list)))


def urlencode(url, encode):
    return urllib.quote(url.encode(encode))
