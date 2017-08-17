# multiprocessing-server code

from fib import fib
from socket import *
from multiprocessing import Process

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)

    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        workers = [Process(target=fib_handler, args=(client,)) for i in range(4)]
        for p in workers:
            p.daemon = True
            p.start()

def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print("Closed")

# This starts a server that listens to localhost on port 25000
fib_server(('', 25000))


