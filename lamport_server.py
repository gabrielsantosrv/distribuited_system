import _thread as thread
import socket
import sys
import time

from lamport_utils import *

# we use counter as a global variable to share among clients
global counter
counter = 0

def handle_client(conn, client_ip):
    stop_loop = False
    global counter
    with conn:
        while not stop_loop:
            counter, keep_loop = receive_message(client_ip, conn, counter)
            if not keep_loop:
                break
            msg = "[{}], the Server received your message".format(client_ip)
            counter = send_message(client_ip, conn, counter, msg)
            time.sleep(1)
        conn.close()

def main():
    global counter
    HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
    PORT = 9000  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print('Server started!')
        print('Waiting for clients...')
        while True:
            conn, addr = sock.accept()
            lamport_timestamp = '(LAMPORT_TIMESTAMP={})'.format(counter)
            print('New client {} at {}'.format(addr, lamport_timestamp))
            counter += 1
            thread.start_new_thread(handle_client, (conn, addr))
        sock.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminating...')
        sys.exit(0)