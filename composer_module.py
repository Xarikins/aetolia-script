from core.module import Module
import tempfile
from subprocess import run

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

        with tempfile.NamedTemporaryFile(suffix=".txt") as tf:
            tf.write(text)
            run(["gvim", tf.name])

    def send_buffer(self):
        if not self.filename:
            return

        with open(self.filename, "r") as f:
            content = f.read()
            self.mud.out("Written content: %s" % content)
            self.mud.gmcp("IRE.Composer.SetBuffer", content)

