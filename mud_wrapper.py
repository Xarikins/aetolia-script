try:
    import tf
except ImportError:
    tf = None

def eval(string):
    out = tf.eval if tf else print
    out(string)

def send(string):
    out = tf.send if tf else print
    out(string)

def out(string):
    out = tf.out if tf else print
    out(string)
