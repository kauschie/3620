# TCP server
import socket
import threading

IP = '127.0.0.1'

PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP,PORT))
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')
    num_received = 0
    while True:
        num_received += 1
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}: {address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,num_received))
        client_handler.start()

def handle_client(client_socket, num_received):
    with client_socket as sock:
        n = 0
        fragments = []
        while True:
            chunk = sock.recv(32)
            if not chunk:
                break
            if len(chunk) < 32:
                fragments.append(chunk)
                break
            n += 1
            fragments.append(chunk)
            # print(f"got {n} chunks")

        print("Server Finished receiving Message")
        arr = b''.join(fragments)

        print(f'[*] Received: {len(arr)} Bytes of Data in {n} 32-Byte Chunks')
        decoded_string = arr.decode('utf-8')
        print(f'[*] Beginning 20 Bytes: {decoded_string[:20]}')
        print(f'[*] Ending 20 Bytes: {decoded_string[-20:]}')
        # fill in so sock should send an ACK message
        mystr = f"Server Ack. Server has received {num_received} requests)".encode()
        sock.send(mystr)
        
if __name__ == '__main__':
    main()