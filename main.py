#!/usr/bin/env python3

import requests
import requests_cache
# import sys
from bs4 import BeautifulSoup
from decouple import config
from icecream import ic
from pathlib import Path
from urllib.parse import urljoin

#  env vars
name = config("NAME", default="noaa")
url = config("URL", default="https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/")
dir = config("DOWNLOAD_DIR", default="data")
ext = config("EXT", default=".gz")
ttl = config("TTL", default=300)

# cache the requests to sqlite, expire after n time
if not ttl:
    min = 5
    sec = 60
    ttl = min * sec
requests_cache.install_cache(f"{name}_cache", backend="sqlite", expire_after=ttl)


def get_html(url):
    """Return the html from the url."""

    # headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0"
    }

    # parse url
    res = requests.get(url, headers=headers)

    return res


def read_html(html):
    """Parse html and return the file(s)."""

    # parse html
    soup = BeautifulSoup(html, "html.parser")

    # find all links
    links = soup.find_all("a")

    return links


# TODO: use sys.argv to pass in args vs. env vars
def download_file(url=url, ext=ext, path=dir):
    """Download file from url and save as filename."""

    # get the raw html
    res = get_html(url)

    # read the html
    links = read_html(res.text)

    # print number of links
    total = [link for link in links if link.get("href").endswith(ext)]

    # TODO: flip logic to check if file exists, then download
    # loop through the links, verify the extension, and download the file
    count = 0
    for item in links:
        href = item.get("href")
        if href.endswith(ext):
            file = urljoin(url, href)
            res = requests.get(file)

            if res.status_code != 200:
                ic(res.status_code)
                ic(res.reason)
                ic(res.text)
                continue
            else:
                # save the file if it doesn't exist
                filename = Path(file).name

                if Path(path) / filename:
                    print(f"{filename} already exists.")
                    continue
                else:
                    count += 1
                    print(f"Saving {filename}.")
                    with open(Path(path) / filename, "wb") as f:
                        f.write(res.content)

    print(f"Total files downloaded: {count} out of {len(total)}.")


def main():
    # create a directory for the data
    Path(dir).mkdir(exist_ok=True)

    # invalidate the cache (for testing)
    # requests_cache.clear()

    # download the file
    download_file(url)


if __name__ == "__main__":
    main()
