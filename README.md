# CSWSH
A command-line tool designed to test and connect to a WebSocket which are vulnerable to Cross-Site WebSocket Hijacking vulnerability.

### About
CSWSH tool can connect to both standard and socket.io based WebSockets.
 - A standard websocket will have the functionality of sending messages to the server and receiving messages from the server.
 - A socket.io based websocket will have only the ping functionality to check if the connection is successful or not.
 
### Requirements
CSWSH works with `Python 3` and has few dependencies.

To install these dependencies, navigate to the source directory and execute `pip3 install -r requirements.txt`

### Usage
CSWSH tool provides the below options while connecting to a websocket server.

#### For standard websocket
```bash
$ python3 cswsh.py "wss://echo.websocket.org"
``` 

#### For socket.io based websocket
```bash
$ python3 cswsh.py "https://example.com/socket.io/" -sio
```
On successful connect, send websocket ping message `2probe` and server will respond with `3probe` as an acknowledgment of the successful connection.

#### Add custom headers
To add custom headers in the request use `-h` option
```bash
$ python3 cswsh.py "wss://echo.websocket.org" -h "Authorization: Bearer AbCdEf123456"
```

#### Add cookies
To add cookies in the request use `-c` option
```bash
$ python3 cswsh.py "wss://echo.websocket.org" -c "sessionID=AbCdEf123456"
```

#### Change Origin 
To add custom origin header in the request use `-o` option
```bash
$ python3 cswsh.py "wss://echo.websocket.org" -o "http://localhost:8080"
```

#### Disable SSL certificate verification
If you don't want the tool to verify the server certificate, use `-i` option
```bash
$ python3 cswsh.py "wss://echo.websocket.org" -i
```


### Support
If you would like to show some support, please connect with me on [twitter](https://twitter.com/_dspawar)
