
import socket
# TCP Client
target_host = '127.0.0.1'
target_port = 9998

def start_tcp_client():
    # create a tcp/ip socket
    # fill in to create a tcp/ip socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect the socket to the server'r address and port
    # fill in to set up the server address
    print(f'[*client*] Connecting {target_host} port {target_port}')
    # fill in to connect the client to the server
    client_socket.connect((target_host, target_port))

    try:
        # send data
        big_str = str([i for i in range(8192)])
        big_data = big_str.encode()
        print(f'[*client*] size of data being sent: {len(big_data)}')  # 48,042 Bytes
        print(f'[*client*] Beginning 20 Bytes: {big_str[:20]}')
        print(f'[*client*] Ending 20 Bytes: {big_str[-20:]}')
        print(f"[*client*] Sending now...")
        client_socket.sendall(big_data)

        # look for the response
        amount_received = 0
        amount_expected = len(big_data)
        while amount_received < amount_expected:
            data = client_socket.recv(16)
            amount_received += len(data)
            print(f"\rReceived {amount_received} of {amount_expected} bytes", end="")
    finally:
        print('\nClosing socket')
        client_socket.close()

start_tcp_client()






