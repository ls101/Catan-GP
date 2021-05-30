# This module contains constants, lists of strings that are used in multiple
# files.  It's safer to import it than rewrite it, as a misspelled string
# will cause errors.

WINNING_NUM = 10
MIN_LARGEST_ARMY = 3
# NUM_PLAYERS = 2  # for faster debugging
NUM_PLAYERS = 4

RESOURCE_NAMES = ["desert", "brick", "ore", "hay", "wood", "sheep"]


def rp():
    string_output = "Please choose the number corresponding to the resource\n"
    for index in range(1, 6):
        string_output += "{}-{} ".format(index, RESOURCE_NAMES[index])
    return string_output


RESOURCES_PRINT = rp()

DEVELOPMENT_CARD_NAMES = [
    "knight", "victory point", "road building", "year of plenty",  "monopoly"]
PORTS_NAMES = ["3:1", "2brick:1", "2ore:1", "2hay:1", "2wood:1", "2sheep:1"]
PLAYER_COLORS = ['red', 'blue', 'white', 'orange']

# PRICES can be used as the "what" argument for the move method, moving cards
# to the bank. It's also used to check if a player can buy a resource, before
# attempting to move.
# Really, this should use indices from the RESOURCE_NAMES list.
PRICES = {
    'dev_card': {
        'brick': 1,
        'ore': 1,
        'sheep': 1
    },

    'roads': {
        'wood': 1,
        'brick': 1
    },

    'settlements': {
        'wood': 1,
        'brick': 1,
        'sheep': 1,
        'hay': 1
    },

    'cities': {
        'ore': 3,
        'hay': 2
    }
}


