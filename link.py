#!/usr/bin/env python
from requests import ConnectionError, get
from pyquery import PyQuery as pq
from urlparse import urlparse
import sys


def getlinks(url, selector):
    parent = urlparse(url)
    try:
        r = get(url)

    except ConnectionError:
        print("Could not connnect to the internet\n")

    links = []
    if r.status_code == 200:
        d = pq(r.text)
        for e in d(selector):
            u = urlparse(pq(e).attr('href'))
            if u.hostname is None:
                links.append(parent.scheme+"://"+parent.netloc + u.geturl())
            else:
                links.append(u.geturl())
    else:
        print("request not complete")
    return links


def link_helper(root, sno):
    try:
        links = getlinks(root, sys.argv[sno])
        for link in links:
            link_helper(link, sno + 1)
    except:
        print root


def main():
    n = len(sys.argv)
    if(n < 3):
        sys.stderr.write("minimum 2 arguments required1.url selectors\
        for subsequent pages")
        sys.exit(1)
    url = sys.argv[1]
    link_helper(url, 2)


if __name__ == '__main__':
    main()
