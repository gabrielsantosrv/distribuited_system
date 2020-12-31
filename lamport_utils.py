"""
Reference: https://towardsdatascience.com/understanding-lamport-timestamps-with-pythons-multiprocessing-library-12a6427881c6
"""


import json


def compute_receive_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1

def send_message(client_ip, sock, counter, msg):
    """
    Send method

    :param client_ip: client IP
    :param sock: socket object
    :param counter: global counter
    :param msg: message to be sent
    :return:
    """
    counter += 1
    data = json.dumps({"message": msg, "timestamp": counter})
    sock.send(data.encode())

    lamport_timestamp = '(LAMPORT_TIMESTAMP={})'.format(counter)
    print('Message sent to {} at {}'.format(client_ip, lamport_timestamp))
    return counter


def receive_message(client_ip, sock, counter):
    """
    Non blocking receive method

    :param client_ip: client IP
    :param sock: socket object
    :param counter: global counter
    :return: updated counter and True if it received something, False otherwise
    """
    is_receive = True
    try:
        data = sock.recv(1024)
        data = json.loads(data.decode())
        message = data.get("message")
        timestamp = data.get("timestamp")
        print('timestamp', timestamp, 'counter', counter)
        counter = compute_receive_timestamp(timestamp, counter)

        lamport_timestamp = '(LAMPORT_TIMESTAMP={})'.format(counter)
        print('Message: {} - received from {} at {}'.format(message, client_ip, lamport_timestamp))

    except ValueError:
        is_receive = False
        print('There is nothing to receive')

    return counter, is_receive

def event(counter):
    counter += 1
    lamport_timestamp = '(LAMPORT_TIMESTAMP={})'.format(counter)
    print('New Event at {}'.format(lamport_timestamp))

    return counter
