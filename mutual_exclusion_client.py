"""
References:
    LAMPORT TIMESTAMP: https://towardsdatascience.com/understanding-lamport-timestamps-with-pythons-multiprocessing-library-12a6427881c6
    TCP SOCKET: https://steelkiwi.com/blog/working-tcp-sockets/
"""
import json
import sys
import time
import urllib.request
import socket


if __name__ == '__main__':
    n_events = int(sys.argv[1])
    sleep_time = int(sys.argv[2])

    # Server IP and PORT
    SERVER_IP = str(sys.argv[3])
    SERVER_PORT = 9000

    counter = 0
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print('My IP address is: ', external_ip)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_IP, SERVER_PORT))
        for i in range(n_events):
            print("Request permission")
            data = json.dumps({"message": "permission"})
            sock.send(data.encode())

            data = sock.recv(1024)
            data = json.loads(data.decode())
            message = data.get("message")

            if message == 'running':
                data = json.dumps({"message": "running", "value": True})
                sock.send(data.encode())
                value = False
            else:
                value = data.get("value")
                print("Permission:", value)

            time.sleep(sleep_time)
            data = json.dumps({"message": "release", "value": True})
            sock.send(data.encode())
            if bool(value):
                print("Releasing permission...")