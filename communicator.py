import mud_wrapper as tf

class Communicator():

    def send(self, message):
        return tf.send(message)

    def eval(self, script):
        return tf.eval(script)
