import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print(f"Listening on PORT: {SERVER_PORT}...")


def get_response(path):
    if path == "/":
        with open("index.html", "r") as fin:
            content = fin.read()
        return "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + content
    elif path == "/programmer":
        with open("programmer.json", "r") as fin:
            content = fin.read()
        return "HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + content
    else:
        with open("Error.html", "r") as fin:
            content = fin.read()
        return "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n" + content


while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1500).decode()
    print(request)
    headers = request.split("\n")
    print(f"Headers: {headers[0]}!!!")
    first_header_components = headers[0].split()

    http_method = first_header_components[0]
    path = first_header_components[1]

    if http_method == "GET":
        response = get_response(path)
    else:
        response = "HTTP/1.1 405 Method Not Allowed\nAllow: GET"

    client_socket.sendall(response.encode())
    client_socket.close()
