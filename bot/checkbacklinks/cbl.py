import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def checkindex(url, anchor, target_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }
    searches = [
        "http://xmlriver.com/search/xml?user=4740&key=ccb9600bfb196581ba2d0e06f1fff0210b39b3e2&query=site:",
        "http://xmlriver.com/search/xml?user=4740&key=ccb9600bfb196581ba2d0e06f1fff0210b39b3e2&query=inurl:",
        "http://xmlriver.com/search/xml?user=4740&key=ccb9600bfb196581ba2d0e06f1fff0210b39b3e2&query="
    ]

    for search in searches:
        r = requests.get(search + url, headers=headers)
        root = ET.fromstring(r.content)
        found = root.find(".//found")
        if found is not None and found.text == '0':
            return "NOT_INDEXED"

        
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    if soup.find("meta", {"name":"robots", "content":"noindex"}):
        return "NOINDEX"

    canonical = "CANONICAL_OK"
    link_canonical = soup.find("link", {"rel":"canonical", "href":True})

    if link_canonical:
        href = link_canonical['href']
        if href != url and not href.endswith("#" + url):
            canonical = "BAD_CANONICAL"
    else:
        canonical = "CANONICAL_NOT_SET"

    redirected = "NOT_REDIRECTED"
    if response.status_code >= 300 and response.status_code < 400:
        redirected = "REDIRECTED"
    
    ok = "BAD"
    if anchor and anchor in response.text:
        ok = "OK"
        if f'href="{anchor}" rel="nofollow"' in response.text:
            ok = "NOFOLLOW"
    
    bad_anchor = ""
    if target_url and target_url in response.text and target_url != anchor:
        bad_anchor = "BAD_ANCHOR"
    
    result = ok
    if bad_anchor and ok == "OK":
        result += "|" + bad_anchor
    if canonical != "CANONICAL_OK":
        result += "|" + canonical
    if redirected != "NOT_REDIRECTED":
        result += "|" + redirected

    return result