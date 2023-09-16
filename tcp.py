import socket
import threading

cookies = {}

def file_name(request):
    header = request.split('\n')
    filename = header[0].split()[1]
    method = header[0].split()[0]
    
    if method == 'GET':
        if filename == '/':
            filename = '/index.html'
            
        try:
            with open('pages' + filename, 'rb') as f:
                content = f.read()
            response = 'HTTP/1.1 200 OK\n'
            response += 'Content-Length: {}\n'.format(len(content))
            response += 'Content-Type: text/html\n'
              
            
            if 'name' in cookies:
                response+= 'Set-Cookie: name = {}\n'.format(cookies['name'])
                
            if 'message' in cookies:
                response+= 'Set-Cookie: message = {}\n'.format(cookies['message'])
                
            response += '\n'
            response = response.encode() + content
            print("GET method is used")
        except FileNotFoundError:
            response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
            response = response.encode()
            
    elif method == 'POST':
        try:
            if filename == '/submit':
                data = request.split('\r\n\r\n', 1)[-1]
                
                name = data.split('&')[0].split('=')[1]
                message = data.split('&')[1].split('=')[1]
                cookies['name'] = name
                cookies['message'] = message
                print(cookies)
                response = 'HTTP/1.1 302 Found\n'
                response += 'Location: /home.html\n'  
                response = response.encode()
                print("POST method is used")
        except Exception as e:
            print(f"Error handling POST request: {e}")
            
    else:
        response = 'HTTP/1.1 405 METHOD NOT ALLOWED\n\nMethod not allowed'
        response = response.encode()
    
    return response

def handle_client(client_socket):
    request = b''
    while True:
        packets = client_socket.recv(1024)
        if not packets:
            break
        request += packets
        if b'\r\n\r\n' in request:
            break

    request = request.decode()
    print(request)

    
    if not request:
        client_socket.close()
        return

    response = file_name(request)

    client_socket.sendall(response)
    client_socket.close()

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8090

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created successfully")
except socket.error as err:
    print("Socket creation failed due to error %s" % (err))

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
except socket.error as err:
    print("Binding failed due to error %s" % (err))

try:
    server_socket.listen(5)  
    print('Listening on port %s ...' % (SERVER_PORT))
except socket.error as err:
    print("Listening failed due to error %s" % (err))

while True:
    try:
        client_connection, client_address = server_socket.accept()
        
        client_handler = threading.Thread(target=handle_client, args=(client_connection,))
        client_handler.start()
    except Exception as e:
        print('Error:', e)

server_socket.close()
