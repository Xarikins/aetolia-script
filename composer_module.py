from core.module import Module
from subprocess import call
import tempfile
import state

class ComposerModule(Module):

    def __init__(self, *args):
        super(ComposerModule, self).__init__(*args)
        self.filename = ""

        self.state["callback_handler"].registerGmcpCallback(\
                "IRE.Composer.Edit", self.content_received)

        self.state["alias_builder"].build({
            "writebuffer": self.send_buffer,
            })

    def content_received(self, content):
        title = content["title"]
        text = content["text"]
        self.mud.out("Received title: '%s'" % title)
        self.mud.out("Received text:")
        self.mud.out(text)

        with tempfile.NamedTemporaryFile(suffix=".txt", mode="wt") as tf:
            self.filename = tf.name
            self.mud.out("Created tempfile: %s" % self.filename)
            tf.write(text)
            tf.flush()
            call(["gvim", tf.name])
            tf.seek(0)

    def send_buffer(self):
        if not self.filename:
            return

        with open(self.filename, "r") as f:
            content = f.read()
            self.mud.out("Written content: %s" % content)
            self.mud.gmcp("IRE.Composer.SetBuffer", content)

if __name__ == "__main__":
    st = state.new()
    comp = ComposerModule(st)
    comp.content_received({"title": "Title", "text": "Some random content"})
