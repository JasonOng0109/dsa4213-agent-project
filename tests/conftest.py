"""Every test runs offline: any attempt to open a socket fails loudly."""

import socket


def _no_network(*a, **k):
    raise AssertionError("network call attempted")


socket.socket.connect = _no_network
socket.create_connection = _no_network
