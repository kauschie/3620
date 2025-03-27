#UDP server
import socket
from time import sleep

def start_udp_server():
    # create udp/ip socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind the socket to the address and port
    server_address = ('localhost', 65423)
    print('starting up on {} port {}'.format(*server_address))
    server_socket.bind(server_address)

    while True:
        # wait for message
        print('Waiting for a message')
        # fill in so server receive the data from the client server_socket.recvfrom(4096) method
        data, address = server_socket.recvfrom(4096)
        print('Received {} bytes from {}'.format(len(data), address))
        print(data)

        if data:
            sent = server_socket.sendto(data, address)
            print('Sent {} bytes back to {}'.format(sent, address))

        sleep(1)

if __name__ == '__main__':
    start_udp_server()
# This is the server code for the UDP server.
# The server code creates a socket and binds it to a port.
# The server code then waits for a message from the client.
# The server code receives the message and sends a response back to the client.
# The server code prints the message and the response.
# The server code closes the socket after sending the response.
