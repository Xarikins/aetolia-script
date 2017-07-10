try:
    import tf
except ImportError:
    tf = None

def eval(string):
    if tf:
        tf.eval(string)
    else:
        print(string)

def send(string):
    if tf:
        tf.send(string)
    else:
        print(string)

def out(string):
    if tf:
        tf.out(string)
    else:
        print(string)
