import requests
import re
from bs4 import BeautifulSoup, element


def getHTML(url):
    try:
        content = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"})
        print('Landed on', url, 'with status code', content.status_code)
        return content.text
    except ValueError:
        print('Invalid URL provided')
        exit()


html = getHTML('https://www.lightnovelworld.com/novel/i-alone-level-up-solo-leveling-web-novel/chapter-232')

soup = BeautifulSoup(html, 'html.parser')

# Grab title
title = soup.find('h2').string

# Grab body of content
box = soup.find('div', class_='chapter-content')

# Decompose unnecessary tags
for tag in box.find_all('div', {'class': ['adsbox', 'vl-ad']}):
    tag.decompose()

print(box)

body = '<h1>{}</h1>'.format(title) + str(box)

