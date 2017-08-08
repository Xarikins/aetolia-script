import mud_wrapper as tf
import json

class Communicator():

    def send(self, message):
        return tf.send(message)

    def eval(self, script):
        return tf.eval(script)

    def out(self, script):
        return tf.out(script)

    def echo(self, string):
        tf.eval("/echo %s" % string)

    def echop(self, string):
        tf.eval("/echo -p %s" % string)

    def info(self, msg):
        self.print_box(msg, "blue")

    def warn(self, msg):
        self.print_box(msg, "yellow")

    def panic(self, msg):
        self.print_box(msg, "red")

    def gmcp(self, key, body):
        payload = body
        if type(body) == dict or type(body) == list:
            payload = json.dumps(body)
        payload = payload.replace("\"", "\\\\\"")
        tf.eval('/test gmcp(\\"%s %s\\")' % (key, payload))

    def print_box(self, msg, color):
        border = "+-" + ("-" * len(msg)) + "-+"
        tf.eval("/echo -aC%s %s" % (color, border))    
        tf.eval("/echo -aC%s %s" % (color, ("| " + msg + " |")))    
        tf.eval("/echo -aC%s %s" % (color, border))    
