#!/usr/bin/env python3

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

    root = "~/src/archive/"
    archive_filename = "archive.json"
    d_root = norm_path(root)
    f_main = norm_path(root + archive_filename)
    f_new = norm_path(root + "archive.json_new")

    with open(f_main, 'r+') as f:
        try:
            current = json.load(f)
        except json.JSONDecodeError:
            current = []

    current.append({'url': to_archive, 'title': page.title.string, 'date': arrow.get().timestamp})

    with open(f_new, 'w') as f:
        json.dump(current, f, indent=2)

    shutil.copy(f_new, f_main)
    os.remove(f_new)

    os.chdir(d_root)
    os.system('git commit -m "Auto-update of archive" "%s"' % archive_filename)
    os.system('git push origin master')
    logging.info("Committed and pushed!")

if __name__ == "__main__":
    main()
