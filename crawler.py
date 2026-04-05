import requests
from bs4 import BeautifulSoup

def get_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }
        response = requests.get(url, headers)
        if response.status_code == 200:
            return response
        else:
            return None
    except Exception as e:
        if "Invalid URL" in str(e):
            return None


def crawl(url, url_crawled):
    tlds = ["co.il", "gov.il", "com", "tech"]
    html_obj = get_url(url)
    url_crawled.add(url)
    if html_obj:
        soup = BeautifulSoup(html_obj.text, "html.parser")
        urls = soup.find_all("a")
        for a_tag in urls:
            try:
                for tld in tlds:
                    if tld in a_tag["href"]:
                        tld_count = a_tag["href"].count(tld)
            
                if base_domain in a_tag["href"] and "#" not in a_tag["href"] and tld_count == 1:
                    if a_tag["href"] not in urls_found:
                        if get_url(a_tag["href"]):
                            urls_found.append(a_tag["href"])

            except KeyError as e:
                pass

        for link in urls_found:
            if link not in url_crawled:
                crawl(link, url_crawled)

        return urls_found

urls_found = []
url_crawled = set()
url = "http://somewebsitesomewhere.co.il"
base_domain = url.split("://")[-1]
crawl(url, url_crawled)
print(urls_found)