
# TCP server
import socket
import threading
from time import sleep

IP = '127.0.0.1'

PORT = 9998

num_threads = 0


def handle_client(connection:socket.socket, client_address:socket.AddressInfo, thread_id:int):
    global num_threads
    try:
        print('Connection from', client_address)
        while True:
            data = connection.recv(16)
            if data:
                print(f'Thread {thread_id} Received {data} ')
                connection.sendall(data)
                sleep(0.2)
            else:
                print('No more data from', client_address)
                break
    finally:
        num_threads -= 1
        print(f'Thread {thread_id} is done. {num_threads} remaining.')
        connection.close()

def start_threaded_tcp_server():
    # Create a TCP/IP socket
    # fill in to create a TCP/IP socket
    # Bind the socket to the address and port
    # fill in for server address
    # bind the server socket to server address
    # Listen for incoming connections
    global num_threads
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP,PORT))
    print(f'[*Server*] Listening on {IP}:{PORT}')
    server_socket.listen(5)
    print('[*Server*] Waiting for a connection...')
    while True:
        connection, client_address = server_socket.accept()
        num_threads += 1
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address, num_threads))
        client_thread.start()
        
if __name__ == '__main__':
    start_threaded_tcp_server()
