from collections import namedtuple

from bs4 import BeautifulSoup
from requests import Session

from switch import HEADERS
from switch.cache import io_cache_with_ttl
from switch.cache import DontCacheException
from switch.web_session import WebSession


class AmazonSession(WebSession, namedtuple('AmazonSession', ['prompt', 'product_id', 'product_description'])):

    # Based upon https://gist.github.com/bryanhelmig/3225bf42e5d2b8fb0cb4b720ac2d3c3b

    POST_URL = 'https://primenow.amazon.com'
    SEARCH_URL = POST_URL + '/search'

    @classmethod
    @io_cache_with_ttl(seconds=600) # Dump cache every ten minutes
    def run_session_for_zipcode(cls, zipcode, prompt):
        print('Performing search query `{:s}` in {:d} ...'.format(prompt, zipcode))
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
            params={'k': prompt},
        )
        if not response.ok:
            raise DontCacheException(response, response.reason)

        return response.text

    @staticmethod
    def check_response_for_product(response, product_id):
        soup = BeautifulSoup(response, 'html.parser')
        div = 'div#house-search-result div#asin-card-{}'.format(product_id)
        return bool(soup.select(div))


def amazon(args):
    for amazon_session in (
        AmazonSession('nintendo switch', 'B01LTHP2ZK', 'Nintendo Switch with Gray Joy-Con'),
        AmazonSession('nintendo switch', 'B01MUAGZ49', 'Nintendo Switch with Neon Blue and Neon Red Joy-Con'),
        AmazonSession('breath of the wild', 'B01MS6MO77', 'The Legend of Zelda: Breath of the Wild - Nintendo Switch'),
        AmazonSession('nintendo switch pro controller', 'B01NAWKYZ0', 'Nintendo Switch Pro Controller'),
    ):
        amazon_session.check_for_zipcode(args.zipcode)
