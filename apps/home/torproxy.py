import socks
import socket
import requests

def make_tor_request(url):
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    response = requests.get(url)
    return response.text
