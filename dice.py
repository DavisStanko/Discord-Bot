import re

# Check if a string is in NdM format
def is_valid_dice_format(string):
    pattern = r"\d+d\d+"
    match = re.fullmatch(pattern, string)
    return match is not None