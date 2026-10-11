# Laborator: funcții, metode și importuri pe web
# Student: <Doru Dan>


BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import argparse
import webtools
from webtools import get_title, security_headers
# Dacă main.py ar avea și o funcție proprie numită get_title, ultima definiție ar înlocui-o pe cea dinainte.
from webtools import DEFAULT_HEADERS, check_paths, save_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help=BASE_URL)
    args = parser.parse_args()

    print(webtools.get_title(webtools.fetch(args.url).text))
    print(DEFAULT_HEADERS)

    paths = ["/", "/robots.txt", "/sitemap.xml"]
    results = webtools.check_paths(args.url, paths)
    webtools.save_report(results)
 

if __name__ == "__main__":
    main()