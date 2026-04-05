import socket

SERVER = "127.0.0.1"
PORT = 1337

client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)

client.connect((SERVER, PORT))

while True:
    inp = input("Enter the operation in the form opreand operator oprenad: ")
    
    if inp == "exit":
        break
   
    client.send(inp.encode())
 
    answer = client.recv(1024)

    print("Answer is "+answer.decode())
    print("Type 'exit' to terminate")
 
client.close()

"""
import socket

HOST = "127.0.0.1"  
PORT = 1337 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    math_problem = input("Enter math problem: ")
    s.sendall(bytes(math_problem, "utf8"))
    data = s.recv(1024)

print(f"\nReceived from Server {data!r}")
"""