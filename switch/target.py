from collections import namedtuple
from json import loads

from cachet import DontCacheException
from cachet import sqlite_cache
from requests import Session

from switch import HEADERS
from switch import TTL
from switch.web_session import WebSession


class TargetSession(
    WebSession,
    namedtuple("TargetSession", ["product_id", "product_description", "is_console"]),
):

    # Based upon https://gist.github.com/rms1000watt/c22cab5aed126824ac0c680fce6669aa

    GET_URL_TEMPLATE = "https://api.target.com/available_to_promise/v2/{:d}/search?key=eb2551e4accc14f38cc42d32fbc2b2ea&nearby={:d}&inventory_type=stores&multichannel_option=none&field_groups=location_summary&requested_quantity=1&radius=100"  # noqa: E501
    IN_STOCK = "IN_STOCK"
    TARGET_HEADERS = {
        "Host": "api.target.com",
        "Origin": "http://www.target.com",
        "Referer": "http://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-52052007?lnk=fiatsCookie",  # noqa: E501
    }

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.prompt = self.product_id

    @classmethod
    @sqlite_cache(ttl=TTL)
    def run_session_for_zipcode(cls, zipcode, product_id):
        cls.info(
            "Performing API call for `{:d}` in {:d} ...".format(product_id, zipcode),
        )
        session = Session()
        session.headers.update(HEADERS)
        session.headers.update(cls.TARGET_HEADERS)

        response = session.get(
            cls.GET_URL_TEMPLATE.format(product_id, zipcode),
        )
        if not response.ok:
            raise DontCacheException(response, response.reason)

        return response.text

    @classmethod
    def check_response_for_product(cls, response, product_id):
        json = loads(response)

        for location in sorted(
            json["products"][0]["locations"],
            key=lambda location: location["distance"],
        ):
            if location["availability_status"] == cls.IN_STOCK:
                name = location["store_name"]
                address = location["formatted_store_address"]
                yield name, address


def target(args):
    print("\n> Target\n")
    for target_session in (
        TargetSession(52052007, "Gray Console", True),
        TargetSession(52189185, "Neon Console", True),
        TargetSession(52161264, "Breath of the Wild", False),
    ):
        target_session.check_for_zipcode(args)
