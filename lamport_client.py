"""
Reference: https://towardsdatascience.com/understanding-lamport-timestamps-with-pythons-multiprocessing-library-12a6427881c6
"""

import sys
import time
import urllib.request
import socket

from lamport_utils import *


def connect(counter, sock, host, port):
    sock.connect((host, port))
    counter += 1
    lamport_timestamp = '(LAMPORT_TIMESTAMP={})'.format(counter)
    print('Connection Request at {}'.format(lamport_timestamp))
    return counter


if __name__ == '__main__':
    # Server IP and PORT
    SERVER_IP = '3.83.227.111'
    SERVER_PORT = 9000
    n_events = int(sys.argv[1])
    sleep_time = int(sys.argv[2])

    counter = 0
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print('My IP address is: ', external_ip)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        counter = event(counter)
        counter = connect(counter, sock, SERVER_IP, SERVER_PORT)
        msg = "Hi there, I am {}".format(external_ip)
        counter = send_message(SERVER_IP, sock, counter, msg)
        counter, _ = receive_message(SERVER_IP, sock, counter)

        for i in range(n_events):
            counter = event(counter)
            time.sleep(sleep_time)

        counter = send_message(SERVER_IP, sock, counter, "bye!")
        counter, _ = receive_message(SERVER_IP, sock, counter)