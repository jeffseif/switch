import json

from requests import post


CONFIGS = None
TEMPLATE = 'https://maker.ifttt.com/trigger/{event:s}/with/key/{key:s}'
VALUES = (
    'value1',  # Description
    'value2',  # Location
    'value3',  # Address
)


def maybe_load_configs(args):
    global CONFIGS
    if CONFIGS is not None:
        return

    if args.config_path is None:
        return

    with open(args.config_path, 'r') as f:
        CONFIGS = json.load(f)


def IFTTT(*values):
    url = TEMPLATE.format(**CONFIGS)
    payload = dict(zip(VALUES, values))
    response = post(
        url=url,
        json=payload,
    )
    print(response.text)


def end_to_end(args):
    if args.config_path is None:
        raise ValueError('Use the --config-path option')
    values = (
        'PRODUCT_NAME',
        'LOCATION',
        'ADDRESS',
    )
    IFTTT(*values)
