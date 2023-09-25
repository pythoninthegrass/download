#!/usr/bin/env python3

import anyio
import httpx
import os
# import requests
# import requests_cache
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

# create a directory for the data
Path(dir).mkdir(exist_ok=True)

# cache the requests to sqlite, expire after n time
if not ttl:
    min = 5
    sec = 60
    ttl = min * sec
# requests_cache.install_cache(f"{name}_cache", backend="sqlite", expire_after=ttl)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0"
}
client = httpx.Client()


def get_html(url):
    """Return the html from the url."""

    # parse url
    res = client.get(url, headers=headers)

    return res


def read_html(html):
    """Parse html and return the file(s)."""

    # parse html
    soup = BeautifulSoup(html, "html.parser")

    # find all links
    links = soup.find_all("a")

    return links


# TODO: use sys.argv to pass in args vs. env vars
async def download_file(links, ext=ext, path=dir):
    """Download file from url and save as filename."""

    count = 0

    # create an async client
    async with httpx.AsyncClient() as client:
        # download the file
        for file in links:
            try:
                filename = Path(file).name
                if Path(f"{path}/{filename}").exists():
                    print(f"{filename} already exists.")
                    continue
                else:
                    count += 1
                    res = await client.get(file, headers=headers)
                    print(f"Saving {filename}.")
                    with open(Path(path) / filename, "wb") as f:
                        f.write(res.content)
            except httpx.HTTPError as e:
                print(f"HTTP Exception for {e.request.url}: {e}")

    print(f"Total files downloaded: {count} out of {len(links)}.")


async def main():
    # invalidate the cache (for testing)
    # requests_cache.clear()

    # get the raw html
    res = get_html(url)

    # read the html
    html = read_html(res.text)

    # loop through the links, verify the extension, and create a list of files
    files = (link for link in html if link.get("href").endswith(ext))
    links = [urljoin(url, file.get("href")) for file in files]

    # download the files
    await download_file(links)


if __name__ == "__main__":
    # main()
    anyio.run(main)
