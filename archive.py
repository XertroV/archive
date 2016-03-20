import requests

import sys, os, shutil
import logging, json

from bs4 import BeautifulSoup
import arrow

logging.basicConfig(level=logging.INFO)


def norm_path(linux_like_path):
    return os.path.expanduser(os.path.normpath(linux_like_path))


def main():
    to_archive = sys.argv[1]
    logging.info('Archiving: %s' % to_archive)
    r = requests.get(to_archive)
    page = BeautifulSoup(r.text, "html.parser")
    logging.info('Page title: %s' % page.title.string)

    f_main = norm_path("~/src/archive/archive.json")
    f_new = norm_path("~/src/archive/archive.json_new")

    with open(f_main, 'a+') as f:
        try:
            current = json.load(f)
        except json.JSONDecodeError:
            current = []

    current.append({'url': to_archive, 'title': page.title.string, 'date': arrow.get().timestamp})

    with open(f_new, 'w') as f:
        json.dump(current, f)

    shutil.copy(f_new, f_main)

    os.remove(f_new)

if __name__ == "__main__":
    main()
