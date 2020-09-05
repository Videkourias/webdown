from urllib.parse import urlparse
import pull, write


def verify(url):
    hostname = urlparse(url).hostname
    sites = ['www.readlightnovel.org', 'www.lightnovelworld.com']

    if hostname in sites:
        return True
    elif not hostname:
        print("Invalid URL")
    else:
        print("No suitable method found")
    return False


def getInfo(url):
    hostname = urlparse(url).hostname
    if hostname == 'www.readlightnovel.org':
        return pull.readlightnovelInit(url)
    elif hostname == 'www.lightnovelworld.com':
        return pull.lightnovelworldInit(url)


def main(info):
    hostname = urlparse(info['url']).hostname

    if hostname == 'www.readlightnovel.org':
        bodies, titles = pull.readlightnovel(info)
        write.createEpub(bodies, titles, info)
    elif hostname == 'www.lightnovelworld.com':
        bodies, titles = pull.lightnovelworld(info)
        write.createEpub(bodies, titles, info)


if __name__ == '__main__':
    main('')
