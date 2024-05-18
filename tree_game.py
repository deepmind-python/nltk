import nltk
from nltk.tokenize import word_tokenize
from nltk import CFG
from nltk.parse import RecursiveDescentParser

# Game map represented as a dictionary
game_map = {
    'entrance': {'north': 'hallway'},
    'hallway': {'south': 'entrance', 'east': 'kitchen', 'west': 'living room'},
    'kitchen': {'west': 'hallway'},
    'living room': {'east': 'hallway'}
}

# Initial player position
player_position = 'entrance'

# List of valid verbs, prepositions, and directions
valid_verbs = ['go', 'move', 'walk', 'head']
valid_prepositions = ['to', 'towards', 'in', 'the direction of']
valid_directions = ['north', 'south', 'east', 'west']
valid_rooms = ['hallway', 'kitchen', 'living room', 'entrance']

# Define a simple grammar for commands
grammar = CFG.fromstring("""
    S -> VP
    VP -> V PP | V NP
    PP -> P NP
    NP -> Det N | N
    V -> "go" | "move" | "walk" | "head"
    P -> "to" | "towards" | "in" | "the" | "direction" | "of"
    Det -> "the"
    N -> "north" | "south" | "east" | "west" | "hallway" | "kitchen" | "living" | "room" | "entrance" | "direction"
""")

# Initialize the parser
parser = RecursiveDescentParser(grammar)

# Function to parse and draw the command tree structure
def draw_command_tree(command):
    tokens = word_tokenize(command.lower())
    try:
        # Parse the command and draw the tree
        for tree in parser.parse(tokens):
            tree.pretty_print()
            tree.draw()
    except ValueError as e:
        print(f"Could not parse command: {e}")

# Function to process commands
def process_command(command):
    tokens = word_tokenize(command.lower())
    if len(tokens) >= 2 and tokens[0] in valid_verbs:
        # Handle commands with just verb and direction (e.g., "go north")
        if tokens[1] in valid_directions:
            return tokens[1]
        # Handle commands with verb, preposition, and direction (e.g., "go to the north")
        elif len(tokens) >= 4 and tokens[1] in valid_prepositions and tokens[3] in valid_directions:
            return tokens[3]
        # Handle commands with verb, preposition, and room (e.g., "move towards the kitchen")
        elif len(tokens) >= 4 and tokens[1] in valid_prepositions and tokens[3] in valid_rooms:
            # Map room names to directions based on current position
            for direction, room in game_map[player_position].items():
                if room == tokens[3]:
                    return direction
    return None

# Function to move player
def move_player(direction):
    global player_position
    if direction in game_map[player_position]:
        player_position = game_map[player_position][direction]
        return f"You moved {direction}. You are now in the {player_position}."
    else:
        return "You can't go that way."

# Function to display help
def display_help():
    return ("Valid commands:\n"
            "'go [direction]', 'move [direction]', 'walk [direction]', 'head [direction]'\n"
            "'go to the [direction]', 'move towards the [room]'\n"
            "Directions: north, south, east, west\n"
            "Rooms: entrance, hallway, kitchen, living room")

# Main game loop
def main_game():
    global player_position
    print(f"You are in the {player_position}.")
    print(display_help())
    while True:
        command = input("Enter command: ")
        if command.lower() == 'help':
            print(display_help())
        else:
            direction = process_command(command)
            if direction:
                result = move_player(direction)
                print(result)
                draw_command_tree(command)
            else:
                print("Invalid command. Type 'help' for a list of valid commands.")
                draw_command_tree(command)  # Draw the tree even for invalid commands

# Run the game
main_game()
