import json
from urllib.parse import urlparse

import click
import requests


def get_sid(url):
    """
    Function to get Session ID of a websocket based on socket.io
    :param url: URL of the Websocket based application
    :return: Websocket URL with session ID
    """
    parsed_url = urlparse(url)

    protocol = parsed_url.scheme
    domain = parsed_url.netloc
    path = parsed_url.path

    uri = protocol + "://" + domain + path

    click.echo("[#] Fetching session ID...")
    response = requests.get(
        uri,
        params={
            'EIO': '3',
            'transport': 'polling',
            't': 'M-LX_vJ'
        }
    )
    sid = json.loads(response.text[4:-4])['sid']
    click.echo("[#] Session ID collected...")

    ws_proto = "ws://"
    if protocol == "https":
        ws_proto = "wss://"

    ws_url = ws_proto + domain + path + "/?EIO=3&transport=websocket&sid=" + sid

    return ws_url
