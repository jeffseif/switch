from collections import namedtuple
from json import loads

from requests import Session

from switch import HEADERS
from switch import LOCATION_TEMPLATE
from switch.cache import io_cache_with_ttl
from switch.cache import DontCacheException
from switch.web_session import WebSession


class WalmartSession(WebSession, namedtuple('WalmartSession', ['product_id', 'product_description'])):

    # Based upon https://gist.github.com/rms1000watt/c22cab5aed126824ac0c680fce6669aa

    AVAILABLE = 'AVAILABLE'
    GET_URL_TEMPLATE = 'https://www.walmart.com/terra-firma/item/{:s}/location/{:d}?selected=true&wl13='
    IN_STOCK = 'IN_STOCK'
    WALMART_HEADERS = {
        'Authority': 'www.walmart.com',
        'Referer': 'https://www.walmart.com/ip/Nintendo-Switch-Gaming-Console-with-Gray-Joy-Con-N-A/55449983',
    }

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.prompt = self.product_id

    @classmethod
    @io_cache_with_ttl(seconds=600) # Dump cache every ten minutes
    def run_session_for_zipcode(cls, zipcode, product_id):
        session = Session()
        session.headers.update(HEADERS)
        session.headers.update(cls.WALMART_HEADERS)

        response = session.get(
            cls.GET_URL_TEMPLATE.format(product_id, zipcode),
        )
        if not response.ok:
            raise DontCacheException(response, response.reason)

        return response.text

    @classmethod
    def check_response_for_product(cls, response, product_id):
        json = loads(response)

        for offer in json['payload']['offers'].values():
            if offer['productAvailability']['availabilityStatus'] == cls.IN_STOCK:
                for location in offer['fulfillment'].get('pickupOptions', []):
                    if location['availability'] == cls.AVAILABLE:
                        name = location['storeName']
                        address = location['storeAddress']
                        yield LOCATION_TEMPLATE.format(name, address)


def walmart(args):
    print('\n> Checking Walmart inventory\n')
    for walmart_session in (
        WalmartSession('2E713IVGQ5JX', 'Nintendo Switch Gaming Console with Neon Blue and Neon Red Joy-Con'),
        WalmartSession('3B092LFMR8PF', 'Nintendo Switch Gaming Console with Gray Joy-Con'),
        WalmartSession('4C90I750L5J3', 'The Legend of Zelda: Breath of the Wild (Nintendo Switch)'),
        WalmartSession('472G702DJ8RK', 'Nintendo Switch Pro Controller'),
    ):
        walmart_session.check_for_zipcode(args.zipcode)
