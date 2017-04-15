from collections import namedtuple

from bs4 import BeautifulSoup
from requests import Session

from switch import HEADERS
from switch.cache import io_cache_with_ttl
from switch.web_session import WebSession


class AmazonSession(namedtuple('AmazonSession', ['query', 'product_id', 'product_description']), WebSession):

    POST_URL = 'https://primenow.amazon.com'
    SEARCH_URL = POST_URL + '/search'

    @classmethod
    @io_cache_with_ttl(seconds=600) # Dump cache every ten minutes
    def run_session(cls, zipcode, query):
        print('Performing query `{:s}` for {:d} ...'.format(query, zipcode))
        session = Session()
        session.headers.update(HEADERS)
        session.post(
            cls.POST_URL,
            data={'newPostalCode': zipcode},
        )
        response = session.get(
            cls.SEARCH_URL,
            params={'k': query},
        )
        print('Done!')
        return response.text

    @staticmethod
    def check_for_product(html, product_id):
        soup = BeautifulSoup(html, 'html.parser')
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
