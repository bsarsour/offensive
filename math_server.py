import socket

def socket_definition():
    host = "127.0.0.1"
    port = 1337
    return (host, port)

def open_socket(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"server listening on:\n{host}:{port}")
    return server_socket

def connection_managment(server_socket):
    conn, addr = server_socket.accept()
    remote_ip_addr, remote_port = addr
    print(f"got connection from:\n{remote_ip_addr}:{remote_port}")
    send_data(conn, "welcome to the awesome calc\n")
    while conn:
        if "close" in recive_data(conn):
            return "close"


def recive_data(conn):
    data = conn.recv(1024)
    if not data: 
        return "close"
    elif "exit" in data.decode("utf-8"):
        send_data(conn, "bye...\n")
        return "close"
    try:
        msg = data.decode("utf-8").strip("\n")
        send_data(conn, f'server: {msg} = {eval(data.decode("utf-8"))}\n')
    except Exception as e:
        print(e)
        send_data(conn, "yamaafan\n")
    return ""


def send_data(conn, msg):
    conn.send(msg.encode())


def close_socket(server_socket):
    server_socket.close()


def main():
    host, port = socket_definition()
    server_socket = open_socket(host, port)
    exit_status = connection_managment(server_socket)
    if "close" in exit_status:
        close_socket(server_socket)



main()
print("Bye..")