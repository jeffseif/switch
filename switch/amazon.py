from collections import namedtuple

from bs4 import BeautifulSoup
from requests import Session

from switch import HEADERS
from switch import TTL
from switch.cache import io_cache_with_ttl
from switch.cache import DontCacheException
from switch.web_session import WebSession


class AmazonSession(WebSession, namedtuple('AmazonSession', ['prompt', 'product_id', 'product_description', 'is_console'])):

    # Based upon https://gist.github.com/bryanhelmig/3225bf42e5d2b8fb0cb4b720ac2d3c3b

    AMAZON_URL_TEMPLATE = 'https://www.amazon.com{:s}'
    POST_URL = 'https://primenow.amazon.com'
    SEARCH_URL = POST_URL + '/search'

    @classmethod
    @io_cache_with_ttl(seconds=TTL)
    def run_session_for_zipcode(cls, zipcode, query):
        cls.info('Performing search query `{:s}` in {:d} ...'.format(query, zipcode))
        session = Session()
        session.headers.update(HEADERS)

        response = session.post(
            cls.POST_URL,
            data={'newPostalCode': zipcode},
        )
        if not response.ok:
            raise DontCacheException(response, response.reason)

        response = session.get(
            cls.SEARCH_URL,
            params={'k': query},
        )
        if not response.ok:
            raise DontCacheException(response, response.reason)

        return response.text

    @classmethod
    def check_response_for_product(cls, response, product_id):
        soup = BeautifulSoup(response, 'html.parser')

        div = 'div#house-search-result div#asin-card-{}'.format(product_id)
        if not soup.select(div):
            return

        for anchor in soup.select('a.a-link-normal'):
            href = anchor.get('href', '')
            if product_id in href:
                yield 'Internet', cls.AMAZON_URL_TEMPLATE.format(href)
                break


def amazon(args):
    print('\n> Amazon\n')
    for amazon_session in (
        AmazonSession('nintendo switch', 'B01LTHP2ZK', 'Gray Console', True),
        AmazonSession('nintendo switch', 'B01MUAGZ49', 'Neon Console', True),
        AmazonSession('breath of the wild', 'B01MS6MO77', 'Breath of the Wild', False),
        AmazonSession('nintendo switch pro controller', 'B01NAWKYZ0', 'Pro Controller', False),
    ):
        amazon_session.check_for_zipcode(args)
