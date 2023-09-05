import socket

def file_name(request):
    header = request.split('\n')
    filename = header[0].split()[1]
    method = header[0].split()[0]
    
    if method =='GET':
        if filename == '/':
            filename = '/index.html'
            
        f = open('pages' + filename)
        content = f.read()
        f.close()
        
        response = 'HTTP/1.0 200 OK\n\n ' + content
    else:
        response = 'HTTP/1.0 405 METHOD NOT ALLOWED\n\nMethod not allowed'   
    
    return response


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print('Listening on port %s ...' % (SERVER_PORT))

while True:
    client_connection , client_address = server_socket.accept()
    
    request = b''
    while True:
        packets = client_connection.recv(1024)
        if not packets:
            break
        request+=packets
        if b'\r\n\r\n' in request:
            break
    
    request = request.decode()
    print(request)
    
    response = file_name(request)
    
    #responses = 'HTTP/1.0 200 OK\n\nHello World'
    client_connection.sendall(response.encode())
    client_connection.close()
    
server_socket.close()