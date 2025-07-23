import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re
import argparse

# 対象のOpenShiftドキュメント
PRODUCT = "openshift_container_platform"
VERSION = "4.19"
BASE_URL = "https://docs.redhat.com/en/documentation/" + PRODUCT + "/" + VERSION

def get_single_page_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.select('a[href]')
    single_page_links = {}

    for link in links:
        href = link.get('href')
        text = link.text.strip()

        # HTML Singleページパス候補検出
        if href and href.startswith("/en/documentation/" + PRODUCT + "/" + VERSION + "/html/"):
            section_base = href.strip('/').replace('/html/', '/html-single/') + "/index"
            single_page_url = urljoin("https://docs.redhat.com/", section_base)

            # 確認のためリクエスト（存在チェック）
            check = requests.head(single_page_url)
            if check.status_code == 200:
                single_page_links[text] = single_page_url
                #print(f"debug: {single_page_url}")

    return single_page_links

if __name__ == "__main__":
    links = get_single_page_links(BASE_URL)
    print("--- OpenShiftドキュメントのシングルページ一覧 ---")
    for name, url in links.items():
        print(f"{url}")
