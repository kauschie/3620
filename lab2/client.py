import socket

# TCP Client
target_host = '127.0.0.1'
target_port = 9998

# create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the client
client.connect((target_host, target_port))

# send some data
big_str = str([i for i in range(8192)])
big_data = big_str.encode()
print(f'size of data being sent: {len(big_data)}')  # 48,042 Bytes
print(f'[*] Beginning 20 Bytes: {big_str[:20]}')
print(f'[*] Ending 20 Bytes: {big_str[-20:]}')
client.send(big_data)
request = client.recv(1024)
print(f'[x] Client Received: {request.decode("utf-8")}')
