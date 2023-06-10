import re
import random

# Check if a string is in NdM format
def is_valid_dice_format(string):
    pattern = r"\d+d\d+"
    match = re.fullmatch(pattern, string)
    return match is not None

# Split string into N and M
def roll_dice(string):
    N = int(string.split("d")[0])
    M = int(string.split("d")[1])
    roll_history = [random.randint(1, M) for i in range(N)]
    roll = sum(roll_history)

    return N, M, roll_history, roll