from message_client import MessageClient
import subprocess
import re

from core.module import Module

class NotificationModule(Module):

    def __init__(self, *args):
        super(NotificationModule, self).__init__(*args)
        self.notifications_enabled = True
        self.message_client = MessageClient("localhost", 12000)

        self.state["alias_builder"].build({
            "notify": self.toggle_notifications,
            })

        self.state["trigger_builder"].build({
            "^(\(.+\))\: (.*)$": {
                "fun": self.trigger_notification,
                "arg": "'%P1' '%P2'",
                },
            })

    def toggle_notifications(self):
        self.notifications_enabled = not self.notifications_enabled
        self.mud.info("Notifications enabled" if self.notifications_enabled else "Notifications disabled")

    def trigger_notification(self, talker, line):
        if self.notifications_enabled:
            subprocess.Popen(["notify-send", "-t", "4", "-i", "/home/linus/muds/aetolia/aet_notify_icon.png", "Aetolia", "%s %s" % (talker, line)])

        color = "white"
        if talker == "(web)":
            color = "red"
        elif talker == "(Sentinels)":
            color = "blue"
        elif talker == "(Duiran)":
            color = "blue"
        elif talker == "(Order)" or talker == "(Congregation)":
            color = "blue"
        elif talker == "(Market)":
            color = "green"
        else:
            color = "yellow"

        self.message_client.send("%s: %s" % (talker,line), color)


