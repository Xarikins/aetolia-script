from socket import *
import json

class MessageClient():

    def __init__(self, addr, port):
        self.addr = (addr, port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(1)

        try:
            self.socket.connect(self.addr)
            self.connected = True
        except:
            self.connected = False


    def send(self, msg, color = "none"):
        if not self.connected:
            pass

        data = {
                "msg": msg,
                "color": color
                }

        packet = json.dumps(data).encode("UTF-8")
        print("Packet size: %d" % len(packet))
        self.socket.sendall(packet)

if __name__ == "__main__":
    client = MessageClient("localhost", 12000)
    client.send("(web): Zoglin says, \"Test message!\"")
    client.send("(web): Zoglin says, \"Test message!\"", "red")
    #client.send("(web): Zoglin says, \"Test message!\"", "green")
    #client.send("(web): Zoglin says, \"Test message!\"", "yellow")
    #client.send("(web): Zoglin says, \"Test message!\"", "blue")
