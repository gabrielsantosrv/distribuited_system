import _thread as thread
import socket
import sys
import time

from lamport_utils import *

def handle_client(conn, client_ip):
    stop_loop = False

    with conn:
        while not stop_loop:
            with open('counter.serialize') as file:
                counter = int(file.readline())

            counter, keep_loop = receive_message(client_ip, conn, counter)
            if not keep_loop:
                break
            msg = "[{}], the Server received your message".format(client_ip)
            counter = send_message(client_ip, conn, counter, msg)

            with open('counter.serialize', 'w') as file:
                file.write(str(counter))

            time.sleep(1)
        conn.close()

def main():
    HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
    PORT = 9000  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print('Server started!')
        print('Waiting for clients...')
        counter = 0
        with open('counter.serialize', 'w') as file:
            file.write(str(counter))

        while True:
            with open('counter.serialize') as file:
                counter = int(file.readline())

            conn, addr = sock.accept()
            lamport_timestamp = '(LAMPORT_TIMESTAMP={})'.format(counter)
            print('New client {} at {}'.format(addr, lamport_timestamp))
            counter += 1

            with open('counter.serialize', 'w') as file:
                file.write(str(counter))
            thread.start_new_thread(handle_client, (conn, addr))
        sock.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminating...')
        sys.exit(0)