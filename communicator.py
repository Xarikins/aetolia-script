import mud_wrapper as tf

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

    def print_box(self, msg, color):
        border = "+-" + ("-" * len(msg)) + "-+"
        tf.eval("/echo -aC%s %s" % (color, border))    
        tf.eval("/echo -aC%s %s" % (color, ("| " + msg + " |")))    
        tf.eval("/echo -aC%s %s" % (color, border))    
