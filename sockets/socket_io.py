import json
from urllib.parse import urlparse

import click
import requests


def get_sid(url, headers, cookies, origin, no_cert_check):
    """
    Function to get Session ID of a websocket based on socket.io
    :param url: URL of the Websocket based application
    :param headers: Custom headers tuple
    :param cookies: Cookies tuple
    :param origin: Set a custom Origin header
    :param no_cert_check: Whether not to verify the server certificate
    :return: Websocket URL with session ID
    """
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    domain = parsed_url.netloc
    path = parsed_url.path
    uri = protocol + "://" + domain + path

    click.echo("[#] Fetching session ID...")

    custom_headers = {}
    req_cookies = {}
    if headers:
        custom_headers = get_object_from_tuple(headers, ':')
    if cookies:
        req_cookies = get_object_from_tuple(cookies, '=')
    if origin:
        custom_headers['Origin'] = origin

    if no_cert_check:
        # disable warning caused by disabled certificate verification
        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning
        )

    try:
        response = requests.get(
            uri,
            params={
                'EIO': '3',
                'transport': 'polling',
                't': 'M-LX_vJ'
            },
            headers=custom_headers,
            cookies=req_cookies,
            verify=not no_cert_check
        )
        response.raise_for_status()
        payload = response.text
        payload = payload[payload.find("{"):payload.rfind("}")+1]
        sid = json.loads(payload)['sid']
        click.echo("[#] Session ID collected...")

        ws_proto = "ws://"
        if protocol == "https":
            ws_proto = "wss://"

        ws_url = ws_proto + domain + path + "/?EIO=3&transport=websocket&sid=" + sid
        return ws_url

    except requests.exceptions.HTTPError as httpErr:
        click.echo("HTTP Error: ", httpErr)
    except requests.exceptions.ConnectionError as connErr:
        click.echo("Connection Error: ", connErr)
    except requests.exceptions.Timeout as timeOutErr:
        click.echo("Connection Timed Out: ", timeOutErr)
    except requests.exceptions.RequestException as reqErr:
        click.echo("Request exception raised: ", reqErr)


def get_object_from_tuple(req_tuple, separator):
    """
    Function to get object from a tuple
    :param req_tuple: A tuple consists of values
    :param separator: Tuple item separator
    :return: An object consists of key-value pair
    """
    req_object = {}
    for item in req_tuple:
        item_array = item.split(separator)
        req_object[item_array[0].strip()] = item_array[1].strip()

    return req_object
