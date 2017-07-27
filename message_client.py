from socket import *
import json

class MessageClient():

    def __init__(self, addr, port):
        self.addr = (addr, port)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.settimeout(1)

    def send(self, msg, color = "none"):
        data = {
                "msg": msg,
                "color": color
                }

        packet = json.dumps(data).encode("UTF-8")
        self.socket.sendto(packet, self.addr)

if __name__ == "__main__":
    client = MessageClient("localhost", 12000)
    client.send("(web): Zoglin says, \"Test message!\"")
    client.send("(web): Zoglin says, \"Test message!\"", "red")
    client.send("(web): Zoglin says, \"Test message!\"", "green")
    client.send("(web): Zoglin says, \"Test message!\"", "yellow")
    client.send("(web): Zoglin says, \"Test message!\"", "blue")
