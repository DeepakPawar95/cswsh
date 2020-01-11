import logging

import click
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


async def create_socket(ws_url, http_url):
    """
    Function to create websocket connection and send messages
    :param ws_url: Websocket URL
    :param http_url: HTTP/HTTPS URL
    """
    url = ws_url
    while True:
        try:
            async with websockets.connect(
                    url, ssl=True
            ) as websocket:

                click.echo("[#] Connection Established...")

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
