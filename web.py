# Import the socket module
from socket import *

# Set the port number for the server to listen on
server_port = 6060

server_socket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
server_socket.bind(('', server_port)) # Bind the server
server_socket.listen(1) # Listen for incoming connections with a maximum queue size of 1
print('The server is ready to listen for requests.')

while True:
    connection_socket, client_addr = server_socket.accept() # Get the connection
    client_ip, client_port = client_addr # Get the IP address & the Port of the client
    sentence = connection_socket.recv(1024).decode() # receive the message and decode it
    print(sentence) # Print the message to the terminal window
    list_of_words = sentence.split(' ') # Split the sentence into words
    request = list_of_words[1][1:]  # extract the name of the request file from the HTTP request
    # Check what is the type of the request and send the appropriate file based on the type
    if  request == 'en' or request == 'index.html' or request == 'main_en' or request == '':
        with open('index.html','rb') as file:
            connection_socket.send("HTTP/1.1 200 OK\r\n".encode())
            connection_socket.send("Content-Type: text/html\r\n".encode())
            connection_socket.send("\r\n".encode())
            content = file.read()
            connection_socket.send(content)
    elif request == 'ar':
        with open('main_ar.html','rb') as file:
            connection_socket.send("HTTP/1.1 200 OK\r\n".encode())
            connection_socket.send("Content-Type: text/html\r\n".encode())
            connection_socket.send("\r\n".encode())
            content = file.read()
            connection_socket.send(content)
    elif request.endswith('.html'):
        with open(request,'rb') as file:
            connection_socket.send("HTTP/1.1 200 OK\r\n".encode())
            connection_socket.send("Content-Type: text/html\r\n".encode())
            connection_socket.send("\r\n".encode())
            content = file.read()
            connection_socket.send(content)
    elif request.endswith('.css'):
        with open(request,'rb') as file:
            connection_socket.send("HTTP/1.1 200 OK\r\n".encode())
            connection_socket.send("Content-Type: text/css\r\n".encode())
            connection_socket.send("\r\n".encode())
            content = file.read()
            connection_socket.send(content)
    elif request.endswith('.png'):
        with open(request,'rb') as file:
            connection_socket.send("HTTP/1.1 200 OK\r\n".encode())
            connection_socket.send("Content-Type: image/png\r\n".encode())
            connection_socket.send("\r\n".encode())
            content = file.read()
            connection_socket.send(content)
    elif request.endswith('.jpg'):
        with open(request, 'rb') as file:
            connection_socket.send("HTTP/1.1 200 OK\r\n".encode())
            connection_socket.send("Content-Type: image/jpg\r\n".encode())
            connection_socket.send("\r\n".encode())
            content = file.read()
            connection_socket.send(content)
    elif request == 'so':
        connection_socket.send('HTTP/1.1 307 Temporary Redirect\r\n'.encode())
        connection_socket.send('Content-Type: text/html\r\n'.encode())
        connection_socket.send('Location: http://stackoverflow.com'.encode())
        connection_socket.send('\r\n'.encode())
    elif request == 'itc':
        connection_socket.send('HTTP/1.1 307 Temporary Redirect\r\n'.encode())
        connection_socket.send('Content-Type: text/html\r\n'.encode())
        connection_socket.send('Location: http://itc.birzeit.edu'.encode())
        connection_socket.send('\r\n'.encode())
    else: # If the requests are other than these, then the file is not found and send an HTTP response saying that.
        html_content=f"""
         <!DOCTYPE html>
         <html lang="en">
         <head>
         <title>Error 404 - Not Found</title>
         </head>
         <body>
         <h1>HTTP/1.1 404 NOT Found</h1>
         <h2>Error 404</h2>
         <p style="color:red;">The file is not found</p>
         <p><strong>Student name : leena abd alrahman </strong></p>
         <p><strong>Student name : alaa nidal</strong></p>
         <p><strong>Student name :shahd walid </strong></p>
         <p><strong>IP and Port: {client_ip}:{client_port}</strong></p>
         </body>
         </html>"""
        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type: text/html\r\n"
        response += "\r\n"
        response +=html_content
        connection_socket.send(response.encode())
    # Close the connection
    connection_socket.close()
