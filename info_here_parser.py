import globals
import re
import combat

PATTERN = "^You can see the following (\d+) objects\\:$"
CPATTERN = re.compile(PATTERN)

running = False
count = 0

VALID_TARGETS = [
        "forager",
        "hunter",
        "lumberjack",
        "umbra",
        "priest",
        ]

def parse_line(line):
    global running, count

    match = CPATTERN.match(line)
    if match:
        running = True
        count = int(match.group(1))
        return

    if not running:
        return

    count -= 1
    if _check_target(line):
        count = 0

    if not count:
        running = False

def _check_target(line):
    for tar in VALID_TARGETS:
        if line.startswith(tar, 1):
            combat.target(line.split()[0].strip('"'))
            return True

    return False

