#!/usr/bin/env python3
from base64 import b64encode
import requests

api_key=""
userhame=""

headers = {
    "Authorization": "Basic {}".format(
        b64encode(bytes(f"{userhame}:{api_key}", "utf-8")).decode("ascii")
        )
        ,
    "Accept": "application/json",
    "X-ExperimentalApi": "opt-in"

}

session = requests.Session()
session.headers.update(headers)

url=""

def paginate(url):

    while url:

        response = session.get(url)
        response.raise_for_status
        api_response=response.json()

        page_number=api_response["pageNumber"]
        page_size=api_response["pageSize"]
        print(page_number,page_size)
        print(response.status_code)

        if page_number < page_size:

            if "&page=" in url:

                next_page = page_number + 1

                base = url.split("&page=")[0]

                next_url=f"{base}&page={next_page}"

                print(next_url)

                paginate(next_url)

            elif not "&page=" in url:

                base = url.split("&page=")[0]

                next_url=f"{base}&page=1"

                print(next_url)

                paginate(next_url)

        url = None

paginate(url)