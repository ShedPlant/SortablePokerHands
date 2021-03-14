VALID_VALUES = {
    "A": {
        "name": "Ace",
        "value": 14
    },
    "K": {
        "name": "King",
        "value": 13
    },
    "Q": {
        "name": "Queen",
        "value": 12
    },
    "J": {
        "name": "Jack",
        "value": 11
    },
    "T": {
        "name": "Ten",
        "value": 10
    },
    "9": {
        "name": "Nine",
        "value": 9
    },
    "8": {
        "name": "Eight",
        "value": 8
    },
    "7": {
        "name": "Seven",
        "value": 7
    },
    "6": {
        "name": "Six",
        "value": 6
    },
    "5": {
        "name": "Five",
        "value": 5
    },
    "4": {
        "name": "Four",
        "value": 4
    },
    "3": {
        "name": "Three",
        "value": 3
    },
    "2": {
        "name": "Two",
        "value": 2
    },
    "a": {
        "name": "AceLow",
        "value": 1
    }
}

class CardValue():
    def __repr__(self): return self.val_as_string

    def __init__(self, val_as_string):
        self.val_as_string = val_as_string

        # This will raise exception if input was invalid
        self.name = VALID_VALUES[val_as_string]["name"]
        self.value = VALID_VALUES[val_as_string]["value"]

    def __lt__(self, other):
        # Counter intuitive but 'less' means 'sort first'
        # Sort higher ranked cards first
        return self.value > other.value

    def __sub__(self, other):
        return self.value - other.value