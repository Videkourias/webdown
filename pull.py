# Contains methods to process data according to URL domain
# Things to note soup.find('whatever').text returns inner text, ignoring all tags
# .string returns the string version of the innerhtml with tags
# ''.join([x for x in soup.find_all()]) will combine all of the returned array nicely
import requests, time
from bs4 import BeautifulSoup


def getHTML(url):
    try:
        content = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"})
        print('Landed on', url, 'with status code', content.status_code)
        return content.text
    except ValueError:
        print('Invalid URL provided')
        exit()


# Initial data gathering for URL of type 'www.readlightnovel.org/*'
# Returns author, suggested title and description, number of chapters in a dictionary
def readlightnovelInit(url):
    html = getHTML(url)

    soup = BeautifulSoup(html, 'html.parser')

    # Author and title
    title = soup.find('div', class_='block-title').find('h1').string.strip()
    author = ''  # Author not recorded properly on this website

    # Description
    desc = soup.find('div', class_='novel-right').find('div', class_='novel-detail-body')

    # Determine number of chapters
    chapterlist = soup.find_all('div', class_='novel-detail-item')[-1]
    chapters = int(''.join([i for i in chapterlist.find('a').string if i.isdigit()]))

    initial = soup.find('div', class_='tab-content').find('a')['href']

    # debug
    # print('URL: {}\n===\nAuthor: {}\n===\nTitle: {}\n===\nDesc: {}\n===\nChapters: {}\n===\nInitial: {}'.format(url, author, title, desc.text, chapters, initial))

    return {"url": url, "author": author, "title": title, "desc": desc, "chapters": chapters, "initial": initial}


# Actual content pull for URL of type 'www.readlightnovel.org/*'
# Returns the content of each chapter, along with each chapters title
def readlightnovel(info):
    html = getHTML(info['initial'])

    soup = BeautifulSoup(html, 'html.parser')

    chapter_list = soup.find('select').find_all('option')

    # Chapter attribute lists
    titles = []
    bodies = []

    # Parse through chapters
    for ch, link in enumerate([chapter['value'] for chapter in chapter_list], start=1):
        if not link:
            continue

        # Delay to not overload site
        time.sleep(1)

        # Get HTML of new page
        html = getHTML(link)

        soup = BeautifulSoup(html, 'html.parser')

        # Grab title
        title = soup.find('div', class_='block-title').find('h1').contents[1]
        title = title[2:].strip()
        titles.append(title)

        # Grab body of content
        box = soup.find('div', class_='desc')
        #body = ''.join([str(p) for p in box.find_all('p')])

        # Decompose unnecessary tags
        for tag in box.find_all(['center', 'hr', 'script', 'small', 'div']):
            tag.decompose()

        body = '<h1>{}</h1>'.format(title) + str(box.prettify())

        # Add current chapter content to bodies list
        bodies.append(body)

    # Return the gathered information
    return bodies, titles


# Initial data gathering for URL of type 'www.lightnovelworld.com/*'
# Returns author, suggested title and description, number of chapters in a dictionary
def lightnovelworldInit(url):
    html = getHTML(url)

    soup = BeautifulSoup(html, 'html.parser')

    # Author and title
    title = soup.find('h1', class_='novel-title').string
    author = soup.find('span', itemprop='author').string

    # Description
    desc = soup.find('div', class_='summary').find('div', class_='content')

    # Determine number of chapters
    chapters = soup.find('div', class_='header-stats').find('strong').text
    chapters = int(''.join([i for i in chapters if i.isdigit()]))

    # Get URL of initial chapter
    # initial = soup.find('li', attrs={'data-chapterno': '1'}).find('a')['href']
    initial = soup.find('a', id='readchapterbtn')['href']
    initial = url + '/' + initial.split('/')[-1]

    # debug print('URL: {}\n===\nAuthor: {}\n===\nTitle: {}\n===\nDesc: {}\n===\nChapters: {}\n===\nInitial: {
    # }'.format(url, author, title, desc.text, chapters, initial))

    return {"url": url, "author": author, "title": title, "desc": desc, "chapters": chapters, "initial": initial}


# Actual content pull for URL of type 'www.lightnovelworld.com/*'
# Returns the content of each chapter, along with each chapters title
def lightnovelworld(info):

    # Chapter content lists
    titles = []
    bodies = []

    nexturl = info['initial']

    # Parse through chapters
    while nexturl:
        # Delay to not overload site
        time.sleep(3)

        # Get HTML of new page
        html = getHTML(nexturl)

        soup = BeautifulSoup(html, 'html.parser')

        # Grab title
        title = soup.find('h2').string
        titles.append(title)

        # Grab body of content
        box = soup.find('div', class_='chapter-content')

        # Decompose unnecessary tags
        for tag in box.find_all('div', {'class': ['adsbox', 'vl-ad']}):
            tag.decompose()

        body = '<h1>{}</h1>'.format(title) + str(box)

        # Add current chapter content to bodies list
        bodies.append(body)

        # Move to next chapter
        next = soup.find('a', class_='nextchap')

        if len(next['class']) == 1:
            nexturl = info['url'] + '/' + next['href'].split('/')[-1]
        else:
            nexturl = None

    # Return the gathered information
    return bodies, titles
