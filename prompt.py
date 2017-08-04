import re
from core.module import *
from core.prompt_listener import *

class PromptParser(Module, PromptListener):
    PATTERN = "^H\:(\d+) M\:(\d+) Mad\:\d+% Bl\: (\d+) XP:\d+% \[(.+)\]$"
    CPATTERN = re.compile(PATTERN)

    def parse_prompt(self, prompt):
        match = self.CPATTERN.match(prompt)
        if not match:
            #self.mud.out("Unmatched prompt: %s" % prompt)
            return

        player = self.state["player"]
        player["health"] = int(match.group(1))
        player["mana"] = int(match.group(2))
        player["bleeding"] = int(match.group(3))

        stats = match.group(4).split()
        index = 0
        if len(stats) > 2:
            player["cloaked"] = "c" in stats[index]
            player["fangbarrier"] = "s" in stats[index]
            player["prone"] = "p" in stats[index]
            player["deaf"] = "d" in stats[index]
            player["blind"] = "b" in stats[index]
            index += 1

        player["equilibrium"] = "e" in stats[index]
        player["balance"] = "b" in stats[index]

        index += 1
        player["lbalance"] = "l" in stats[index]
        player["rbalance"] = "r" in stats[index]

        #print(str(player))
