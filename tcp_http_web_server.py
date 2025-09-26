from socket import *
from datetime import datetime, timezone

#Create a TCP server socket
port = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))  # Bind the server to all available interfaces on the specified port
serverSocket.listen(1)  # Puts the socket in listening mode (max queue: 1)

while True:
    #Establish the connection
    print("The server is ready to receive")
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open("./html_files/index.html")
        outputdata = f.read()

        # Build HTTP 200 OK response headers
        # Set-Cookie is used to store a cookie on the client browser with name 'coursename' and value 'CompNet'
        # Max-Age sets cookie expiry time (in seconds), currently set to 7 days = 604800s
        now = datetime.now(timezone.utc).strftime("Date: %a, %d %b %Y %H:%M:%S GMT")
        output_bytes = outputdata.encode('utf-8')

        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            f"{now}\r\n"
            "Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {len(output_bytes)}\r\n"
            "Set-Cookie: coursename=CompNet; Path=/; HttpOnly; Max-Age=604800\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        # Send response headers
        connectionSocket.send(response_headers.encode('utf-8'))

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        # Close the socket
        connectionSocket.close()

    except IOError:
        # If file not found, return a 404 Not Found response
        now = datetime.now(timezone.utc).strftime("Date: %a, %d %b %Y %H:%M:%S GMT")
        body = ("<html><body><h1>404 Not Found</h1></body></html>")
        not_found_bytes = body.encode('utf-8')

        not_found_headers = (
            "HTTP/1.1 404 Not Found\r\n"
            f"{now}\r\n"
            "Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {len(not_found_bytes)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        # Send 404 response headers and body
        connectionSocket.send(not_found_headers.encode('utf-8'))
        connectionSocket.send(not_found_bytes)

        # Close the socket
        connectionSocket.close()

# Close the server socket
serverSocket.close()