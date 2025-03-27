#UDP client
import socket

def start_udp_client():
    # Create udp/ip socket
    # fill in to create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # server address
    server_address = ('localhost', 65423)

    for i in range(3):
        try:
            message = f'This is message {i+1}. It will be repeated.'.encode()
            # send data
            print('sending {!r}'.format(message))
            sent = client_socket.sendto(message, server_address)
            
            # receive response
            print('client waiting to receive response')
            # fill in so client receives the data from the server using the client_socket.recvfrom(4096) method
            data, server = client_socket.recvfrom(4096)

            print(f'Received {data} from {server}')
        except:
            print(f'error sending message {i}')
        
    print('closing socket')
    client_socket.close()

if __name__ == '__main__':
    start_udp_client()
# This is the client code for the UDP server. 
# The client sends a message to the server and waits for a response. 
# The client code is similar to the server code (udp_server.py), 
#   but it sends a message to the server and waits for a response. 
# The client code creates a socket and sends a message to the server. 
# The client code then waits for a response from the server and prints the response. The client code closes the socket after receiving