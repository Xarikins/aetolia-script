import re
from core.module import *
from core.prompt_listener import *

class PromptParser(Module, PromptListener):
    PATTERN = "^H\:(\d+) M\:(\d+) Bl\: (\d+) XP:\d+% \[(.+)\]$"
    CPATTERN = re.compile(PATTERN)

    def parse_prompt(self, prompt):
        match = self.CPATTERN.match(prompt)
        if not match:
            return

        player = self.state["player"]
        player["health"] = int(match.group(1))
        player["mana"] = int(match.group(2))
        player["bleeding"] = int(match.group(3))

        stats = match.group(4).split()
        player["fangbarrier"] = "s" in stats[0]
        player["prone"] = "p" in stats[0]
        player["deaf"] = "d" in stats[0]
        player["blind"] = "b" in stats[0]
        player["balance"] = "b" in stats[1]
        player["equilibrium"] = "e" in stats[1]
        player["lbalance"] = "l" in stats[2]
        player["rbalance"] = "r" in stats[2]

        #print(str(player))
