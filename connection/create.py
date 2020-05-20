import logging

import click
import ssl
import websockets

import sockets.socket_io as socket_io


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


async def create_socket(ws_url, http_url, headers, cookies, origin, no_cert_check):
    """
    Function to create websocket connection and send messages
    :param ws_url: Websocket URL
    :param http_url: HTTP/HTTPS URL
    :param headers: Custom headers tuple
    :param cookies: Cookies tuple
    :param origin: Set a custom Origin header
    :param no_cert_check: Whether not to verify the server certificate
    """
    url = ws_url
    ctr = 0

    custom_headers = {}
    if headers:
        custom_headers = get_object_from_tuple(headers, ':')
    if cookies:
        custom_headers['Cookie'] = '; '.join(cookies)
    if origin:
        custom_headers['Origin'] = origin

    while True:
        try:
            async with websockets.connect(
                    url,
                    ssl=ssl._create_unverified_context() if no_cert_check else True,
                    extra_headers=custom_headers
            ) as websocket:

                click.echo("[#] Connection Established...")
                if ctr == 0:
                    ctr += 1
                    show_vulnerable_msg()

                while True:
                    client = input("\n" + Colors.OKBLUE + "[CLIENT] => " + Colors.ENDC)
                    await websocket.send(client)

                    server = await websocket.recv()
                    print(Colors.OKGREEN + "[SERVER] <= " + Colors.ENDC + server)

        except websockets.ConnectionClosed as excClosed:
            click.echo("[#] Connection Closed. Restarting connection...")
            url = socket_io.get_sid(http_url)
            continue

        except websockets.InvalidStatusCode as excStatus:
            logging.error('Invalid Status')
            logging.error(excStatus)

        except Exception as exc:
            logging.error('Exception occurred')
            logging.error(exc)


def show_vulnerable_msg():
    click.echo(Colors.FAIL + "\n#################################################" + Colors.ENDC)
    click.echo(Colors.FAIL + "   Vulnerable to Cross Site WebSocket Hijacking" + Colors.ENDC)
    click.echo(Colors.FAIL + "#################################################" + Colors.ENDC)


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
