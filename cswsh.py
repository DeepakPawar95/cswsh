#!/usr/bin/env python

import asyncio

import click
from pyfiglet import Figlet

import connection.create as connection
import sockets.socket_io as socket_io


@click.command()
@click.argument('url')
@click.option('--type', '-t', type=click.Choice(['1', '2']), default='1', help='Type of test 1. Standard 2. Socket IO')
@click.option('--header', '-h', multiple=True, help='Add a custom header')
@click.option('--cookie', '-c', multiple=True, help='Set a cookie')
@click.option('--origin', '-o', help='Set a custom Origin')
def main(url, type, header, cookie, origin):
    """
    A pen testing tool to perform Cross-Site WebSocket Hijacking (CSWSH)

    EXAMPLES:  \n
    For standard CSWSH test \n
        $ cswsh "http://example.com"

    For socket.io: \n
        $ cswsh "https://example.com/socket.io/" -t 2
    """
    if type == '2':
        ws_url = socket_io.get_sid(url, header, cookie, origin)
        start_ws(ws_url, url, header, cookie, origin)
    else:
        start_ws(url, url, header, cookie, origin)


def start_ws(ws_url, url, header, cookie, origin):
    """
    Function to start websocket connection
    :param ws_url: Websocket URL
    :param url: Application URL
    :param header: Add custom headers
    :param cookie: Add cookies
    """
    click.echo("[#] Starting Websocket connection...")
    asyncio.get_event_loop().run_until_complete(connection.create_socket(ws_url, url, header, cookie, origin))


if __name__ == "__main__":
    title = Figlet(font='slant')
    print(title.renderText('CSWSH'))
    print('Cross-Site WebSocket Hijacking Pentesting Tool')
    print('Version: 1.0.0')
    print('Creator: Deepak Pawar\n\n')
    main()
