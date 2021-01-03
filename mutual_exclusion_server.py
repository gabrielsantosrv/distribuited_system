"""
References:
    LAMPORT TIMESTAMP: https://towardsdatascience.com/understanding-lamport-timestamps-with-pythons-multiprocessing-library-12a6427881c6
    TCP SOCKET: https://steelkiwi.com/blog/working-tcp-sockets/
"""


import _thread as thread
import socket
import sys
import time

from lamport_utils import *

is_free = True
last_time = 0
def handle_client(sock, client_ip):
    global is_free
    global last_time
    with sock:
        while True:
            try:
                data = sock.recv(1024)
                data = json.loads(data.decode())
                message = data.get("message")
                if message == 'permission':
                    print("Client {} request permission - permission {}".format(client_ip, is_free))
                
                    data = json.dumps({"message": "permission", "value": is_free})
                    sock.send(data.encode())
                    last_time = time.time()
                    if is_free:
                        is_free = False
                    #check_is_alive(sock, client_ip)
                else:
                    print("Client {} release resource".format(client_ip))
                    is_free = True
                check_is_alive(sock, client_ip)
                time.sleep(1)
            except ValueError:
                break

def check_is_alive(sock, client_ip):
    global last_time, is_free
    if last_time > 0:
        diff = time.time() - last_time
        if diff >= 10:  # timeout de 10 segundos
            print("Checking {} health".format(client_ip))
            data = json.dumps({"message": "running"})
            sock.send(data.encode())
            while True:
                try:

                    data = sock.recv(1024)
                    data = json.loads(data.decode())
                    message = data.get("message")
                    if message == 'running':
                        last_time = time.time()
                        print("{} is still running".format(client_ip))
                        break
                except ValueError:
                    # nó morreu
                    is_free = True
                    print("{} is dead".format(client_ip))                    
                    break

def main():
    HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
    PORT = 9000  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print('Server started!')
        print('Waiting for clients...')
        while True:
            conn, addr = sock.accept()

            print('New client {}'.format(addr))
            thread.start_new_thread(handle_client, (conn, addr))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminating...')
        sys.exit(0)
