# This module contains constants, lists of strings that are used in multiple files.
# It's safer to import it than rewrite it, as a misspelled string will cause errors.

RESOURCE_NAMES = ["desert", "brick", "ore", "hay", "wood", "sheep"]
DEVELOPMENT_CARD_NAMES = ["knight","victory point", "road building", "year of plenty",  "monopoly"]
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

    'road': {
        'wood': 1,
        'brick': 1
    },

    'settlement': {
        'wood': 1,
        'brick': 1,
        'sheep': 1,
        'hay': 1
    },
    
    'city': {
        'ore': 3,
        'hay': 2
    }
}