__author__ = 'Jeffrey Seifried'
__description__ = 'Scraping tools for getting me a damn Nintendo Switch'
__email__ = 'jeffrey.seifried@gmail.com'
__program__ = 'switch'
__url__ = 'http://github.com/jeffseif/{}'.format(__program__)
__version__ = '1.0.0'
__year__ = '2017'


HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}
TTL = 1800 # IO caches will be ignored after 30 minutes
