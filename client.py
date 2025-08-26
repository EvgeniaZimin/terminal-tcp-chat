import socket
import threading
import select

client = socket.socket()
chat_link = input('Please enter full chat link: ')
not_yet_host_or_port = chat_link.split('://')[1]
host = not_yet_host_or_port.split(':')[0]
port = int(not_yet_host_or_port.split(':')[1])
client.connect((host, port))


def user_message(client):
    try:
        while True:
            message = input()
            if message == 'pls let me go':
                client.send(message.encode())
                client.close()
            else:
                client.send(message.encode())
    except Exception:
        client.close()
        exit()


def chat_messages(client):
    try:
        while True:
            events_list = [client]
            read_list, write_list, error_list = select.select(events_list, [], [])
            for read in read_list:
                if read == client:
                    message = read.recv(1024).decode()
                    print(message)
    except Exception:
        client.close()
        exit()

chat_thread = threading.Thread(target=chat_messages, args=(client, ))
user_messages = threading.Thread(target=user_message, args=(client, ))
chat_thread.start()
user_messages.start()
