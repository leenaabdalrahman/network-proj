from socket import *

# Set the port number for the server to listen on
server_port = 6060

# Define content types
content_types = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.svg': 'image/svg+xml'
}

def handle_request(connection_socket):
    sentence = connection_socket.recv(1024).decode()  # Receive the message and decode it
    print(sentence)  # Print the message to the terminal window
    list_of_words = sentence.split(' ')  # Split the sentence into words

    request = list_of_words[1][1:]  # Extract the name of the request file from the HTTP request

    if request in ('en', 'index.html', 'main', ''):
        filename = 'index.html'
    elif request == 'ar':
        filename = 'main_ar.html'
    else:
        filename = request

    try:
        with open(filename, 'rb') as file:
            extension = filename[filename.rfind('.'):]
            content_type = content_types.get(extension, 'text/plain')
            content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode() + content
    except FileNotFoundError:
        response = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Error 404 - Not Found</title>
        </head>
        <body>
            <h1>HTTP/1.1 404 NOT Found</h1>
            <h2>Error 404</h2>
            <p style="color:red;">The file is not found</p>
            <p><strong>Student name: leena abd alrahman</strong></p>
            <p><strong>Student name: shahd walid</strong></p>
            <p><strong>Student name: ala nidal</strong></p>
            <p><strong>IP and Port: {client_ip}:{client_port}</strong></p>
        </body>
        </html>""".encode()

    connection_socket.send(response)
    connection_socket.close()

# Create a TCP socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))  # Bind the server
server_socket.listen(1)  # Listen for incoming connections with a maximum queue size of 1
print('The server is ready to listen for requests.')

while True:
    connection_socket, client_addr = server_socket.accept()  # Get the connection
    client_ip, client_port = client_addr  # Get the IP address & the Port of the client
    handle_request(connection_socket)
