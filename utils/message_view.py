from socket import *
from subprocess import call
import time
import json

def listen():
    call("clear")
    server = socket(AF_INET, SOCK_DGRAM)
    server.bind(("", 12000))

    while True:
        data, addr = server.recvfrom(2048)

        if not data:
            continue

        print("%s " % time.strftime("%H:%M:%S", time.localtime()), end="")

        message = json.loads(data.decode("UTF-8"))
        if message["color"].lower() == "red":
            print("\033[31m", end="")
        elif message["color"].lower() == "green":
            print("\033[32m", end="")
        elif message["color"].lower() == "yellow":
            print("\033[33m", end="")
        elif message["color"].lower() == "blue":
            print("\033[34m", end="")

        print(message["msg"], end="")
        print("\033[0m")

if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
