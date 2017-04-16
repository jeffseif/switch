from collections import namedtuple
from json import loads

from requests import Session

from switch import HEADERS
from switch.cache import io_cache_with_ttl
from switch.web_session import WebSession


class TargetSession(WebSession, namedtuple('TargetSession', ['prompt', 'product_description'])):

    IN_STOCK = 'IN_STOCK'
    GET_URL_TEMPLATE = 'https://api.target.com/available_to_promise/v2/{:d}/search?key=eb2551e4accc14f38cc42d32fbc2b2ea&nearby={:d}&inventory_type=stores&multichannel_option=none&field_groups=location_summary&requested_quantity=1&radius=100'
    TARGET_HEADERS = {
        'Host': 'api.target.com',
        'Origin': 'http://www.target.com',
    }
    LOCATION_TEMPLATE = '\033[1;33m{:s}\033[0m: \033[1;90m{:s}\033[0m'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.product_id = self.prompt

    @classmethod
    @io_cache_with_ttl(seconds=600) # Dump cache every ten minutes
    def run_session_for_zipcode(cls, zipcode, prompt):
        print('Performing API call for `{:d}` in {:d} ...'.format(prompt, zipcode))
        session = Session()
        session.headers.update(HEADERS)
        session.headers.update(cls.TARGET_HEADERS)

        response = session.get(
            cls.GET_URL_TEMPLATE.format(prompt, zipcode),
        )
        if not response.ok:
            raise DontCacheException(response, response.reason)

        return response.text

    @classmethod
    def check_response_for_product(cls, response, product_id=None):
        json = loads(response)

        status = False
        for location in sorted(
            json['products'][0]['locations'],
            key = lambda location: location['distance'],
        ):
            if location['availability_status'] == cls.IN_STOCK:
                name = location['store_name']
                address = location['formatted_store_address']
                print(cls.LOCATION_TEMPLATE.format(name, address))
                status = True
        return status


def target(args):
    for target_session in (
        TargetSession(52189185, 'Nintendo® Switch™ with Neon Blue and Neon Red Joy-Con™',),
        TargetSession(52052007, 'Nintendo Switch Gray ???',),
        TargetSession(52161264, 'The Legend of Zelda™: Breath of the Wild™ (Nintendo Switch)',),
    ):
        target_session.check_for_zipcode(args.zipcode)
