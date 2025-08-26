import socket
import select
from _thread import *
from pyngrok import ngrok, conf
import hashlib

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_addr = '0.0.0.0'
print('Welcome to chat server!')
while True:
    port = int(input('Please enter the port number you want your server to run on (0-65535): '))
    
    if int(port) in range(0, 65536):
        break
server.bind((ip_addr, port))
server.listen()
print('To make your server open to everyone, please, register on https://ngrok.com/ to get your free public server.\nThen go to https://dashboard.ngrok.com/get-started/your-authtoken and copy your authtoken.')
authtoken = input('Please enter your ngrok authtoken: ')

ngrok.set_auth_token(authtoken)
public = ngrok.connect(port, 'tcp')
link_for_client = str(public).split('"')[1]
print(f"This is the link you need to give to your clients to access your chat: {link_for_client}")
print('Server is working, waiting for chat participants')
clients_list = []
identified_list = []
usernames_passwords = {"admin" : hashlib.sha256('password'.encode('utf-8')).hexdigest(), 'test1':hashlib.sha256('123456'.encode('utf-8')).hexdigest()}


def username_password(connection, usernames_passwords):
    while True:
        connection.send(b'Please tell us how to call you in chat today\n')
        how_to_call = connection.recv(1024).decode()
        connection.send(f'Please confirm, you want us to call you {how_to_call}? y/n\n'.encode())
        conf = connection.recv(1024).decode()
        if conf.lower() == "y":
            while True:
                connection.send(f'{how_to_call}, do you want to register or sign in? r/s\n'.encode())
                answer = connection.recv(1024).decode()
                if answer.lower() == "s":
                    connection.send(f'{how_to_call}, please, enter your username\n'.encode())
                    user_username = connection.recv(1024).decode()
                    print(user_username)
                    connection.send(f'{how_to_call}, please, enter your password\n'.encode())
                    user_pass = connection.recv(1024).decode()
                    print(user_pass)
                    if user_username in usernames_passwords.keys():
                        if hashlib.sha256(user_pass.encode('utf-8')).hexdigest() == usernames_passwords[user_username]:
                            identified_list.append(connection)
                            connection.send(f'{how_to_call}, welcome!!!\n'.encode())
                            message = f"{how_to_call} entered the chat\n".encode()
                            send_broadcast(message, connection)
                            return user_username, how_to_call
                        else:
                            connection.send(b'Wrong credentials!!!\n')
                    else:
                        connection.send(b"Wrong credentials!!!\n")
                elif answer.lower() == 'r':
                    x = 0
                    while x == 0:
                        connection.send(f'{how_to_call}, please enter desired username\n'.encode())
                        username = connection.recv(1024).decode()
                        if username in usernames_passwords.keys():
                            connection.send(f'Username "{username}" reserved by another user\n'.encode())
                            break
                        else:
                            while True:
                                connection.send(f"{how_to_call}, please, confirm that your desired username is {username} y/n. 'e' to return to main menu\n".encode())
                                answer = connection.recv(1024).decode()
                                if answer.lower() == 'y':
                                    connection.send(f'{how_to_call}, please enter desired password\n'.encode())
                                    password = connection.recv(1024).decode()
                                    connection.send(f'{how_to_call}, please re-enter your password for confirmation purposes\n'.encode())
                                    password_conf = connection.recv(1024).decode()
                                    if password == password_conf:
                                        connection.send(b'Registration complete!\n')
                                        usernames_passwords[username] = hashlib.sha256(password.encode('utf-8')).hexdigest()
                                        print(usernames_passwords[username])
                                        x = 1
                                        break
                                    elif password != password_conf:
                                        connection.send(b"Passwords don't match, please try again\n")
                                        continue
                                elif answer.lower() == 'n':
                                    break
                                elif answer.lower() == 'e':
                                    x = 1
                                    break
                                else:
                                    connection.send(b'Wrong input!\n')
                                    continue
                else:
                    connection.send(b'Wrong input!\n')
                    continue
        if conf.lower() == 'n':
            continue
        else:
            connection.send(b'Wrong input!\n')
            continue
        

def client_thread(connection, address, usernames_passwords):
    try:
        connection.send(b'Welcome to chat!\n')
        username, how_to_call = username_password(connection, usernames_passwords)
        while True:
            try:
                message = connection.recv(1024)
                if message.decode() == 'pls let me go' and connection in identified_list:
                    identified_user_leaving(connection, how_to_call)
                elif message.decode() == 'pls let me go' and connection not in identified_list:
                    not_identified_user_leaving(connection, address)
                elif message:
                   user_message = f'<{how_to_call}> {message.decode()}'
                   print(user_message)
                   send_broadcast(user_message.encode(), connection)
            except Exception:
                continue
    except ConnectionAbortedError:
        not_identified_user_leaving(connection, address)
    except UnicodeDecodeError:
        pass
    except ConnectionResetError:
        not_identified_user_leaving(connection, address)


def not_identified_user_leaving(connection, address):
    message = f'{address} is leaving'
    print(message)
    send_broadcast(message.encode(), connection)
    remove(connection)


def identified_user_leaving(connection, how_to_call):
    message = f'{how_to_call} is leaving'
    print(message)
    send_broadcast(message.encode(), connection)
    remove(connection)



def send_broadcast(message, connection):
    for clients in clients_list:
        try:
            if clients not in identified_list:
                continue
            elif clients == connection:
                clients.send(b'sent broadcast\n')
            else:
                clients.send(message)
        except Exception:
            if client in identified_list:
                identified_user_leaving(client, how_to_call)
            if client not in identified_list:
                not_identified_user_leaving(client, address)




def remove(connection):
    if connection in clients_list:
        if connection in identified_list:
            identified_list.remove(connection)
        connection.close()
        clients_list.remove(connection)


while True:
    connection, address = server.accept()
    clients_list.append(connection)
    print(f"New client {address}")
    start_new_thread(client_thread, (connection, address, usernames_passwords))
