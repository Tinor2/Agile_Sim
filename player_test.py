from roomTemplate import room, Grid, Map
import random

class Player:
    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room
        self.current_cell = (1, 1)  # Start in center of room
        self.inventory = []
    
    def move_within_room(self, direction):
        direction_map = {
            "north": (-1, 0),
            "south": (1, 0),
            "east": (0, 1),
            "west": (0, -1)
        }
        
        if direction not in direction_map:
            return f"Invalid direction. Please choose from: {', '.join(direction_map.keys())}"
        
        delta_row, delta_col = direction_map[direction]
        new_row = self.current_cell[0] + delta_row
        new_col = self.current_cell[1] + delta_col
        
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            # Check if we're at a door position
            if (new_row == 0 or new_row == 2 or new_col == 0 or new_col == 2):
                for door_pos, target_id in self.current_room.doors:
                    if (new_row == 0 and door_pos == "north") or \
                       (new_row == 2 and door_pos == "south") or \
                       (new_col == 0 and door_pos == "west") or \
                       (new_col == 2 and door_pos == "east"):
                        return f"There's a door leading to room {target_id}. Use 'use_door' to go through it."
            
            self.current_cell = (new_row, new_col)
            return f"You moved {direction} to cell {self.current_cell}"
        else:
            return "You can't move that way. You've reached the edge of the room."
    
    def use_door(self, target_room_id):
        # Check if target room is accessible through a door
        for door_pos, door_target in self.current_room.doors:
            if door_target == target_room_id:
                self.current_room = self.current_room.all_rooms[list(self.current_room.all_rooms).index(target_room_id)]
                # Adjust position based on entry direction
                if door_pos == "north":
                    self.current_cell = (2, 1)
                elif door_pos == "south":
                    self.current_cell = (0, 1)
                elif door_pos == "east":
                    self.current_cell = (1, 0)
                else:  # west
                    self.current_cell = (1, 2)
                return f"You entered room {target_room_id}"
        return "There is no door leading to that room from here."
    
    def look_around(self):
        # Generate a description of the current room and cell
        room_desc = f"You are in room {self.current_room.id}, standing in cell {self.current_cell}."
        
        # Check if we're at a cell that might have a door
        doors_info = ""
        if self.current_cell[0] == 0 or self.current_cell[0] == 2 or self.current_cell[1] == 0 or self.current_cell[1] == 2:
            doors_info = "\nYou see doors leading to: "
            available_doors = []
            
            for door in self.current_room.doors:
                # Check door orientation based on current cell
                if (self.current_cell[0] == 0 and self.current_room.id[0] > door[0]) or \
                   (self.current_cell[0] == 2 and self.current_room.id[0] < door[0]) or \
                   (self.current_cell[1] == 0 and self.current_room.id[1] > door[1]) or \
                   (self.current_cell[1] == 2 and self.current_room.id[1] < door[1]):
                    available_doors.append(str(door))
            
            if available_doors:
                doors_info += ", ".join(available_doors)
            else:
                doors_info = "\nThere are no doors nearby."
        
        # Random chance to find an item
        item_info = ""
        if random.random() < 0.3:  # 30% chance to find something
            items = ["rusty key", "old coin", "torn page", "small gem", "wooden token"]
            item = random.choice(items)
            item_info = f"\nYou notice a {item} on the ground. You can 'take' it."
        
        return room_desc + doors_info + item_info
    
    def investigate(self):
        # Generate a more detailed description of the current cell
        descriptions = [
            "The walls are covered in strange symbols.",
            "There's a mysterious pattern etched into the floor.",
            "You notice scratch marks near the corners of this cell.",
            "The air feels slightly colder here.",
            "A faint humming sound can be heard.",
            "The floor tiles in this section are a different color.",
            "This part of the room seems recently disturbed.",
            "Everything appears normal in this section.",
            "A dim light flickers momentarily and then fades.",
            "You sense that something important once happened here."
        ]
        
        # Special descriptions for edge cells
        if self.current_cell[0] == 0 or self.current_cell[0] == 2 or self.current_cell[1] == 0 or self.current_cell[1] == 2:
            edge_descriptions = [
                "The wall here seems slightly different than the others.",
                "You can feel a draft coming from somewhere.",
                "There's a small crack running along the edge of the floor.",
                "This section of the wall looks like it might conceal something."
            ]
            descriptions.extend(edge_descriptions)
        
        # Puzzle hint with 20% probability
        puzzle_hint = ""
        if random.random() < 0.2:
            hints = [
                "There's a small indentation that looks like it could fit a specific object.",
                "You find a note that reads: 'The sequence matters'.",
                "There's a set of symbols that might represent a code.",
                "You notice a mechanism that seems to be part of a larger puzzle.",
                "A subtle arrow points towards another room."
            ]
            puzzle_hint = f"\n{random.choice(hints)}"
        
        return f"You carefully examine the area around you.\n{random.choice(descriptions)}{puzzle_hint}"
    
    def take(self, item):
        # Simplified item collection
        if random.random() < 0.5:  # 50% chance of success
            self.inventory.append(item)
            return f"You picked up the {item} and added it to your inventory."
        else:
            return f"You try to take the {item}, but it's stuck or not actually there."
    
    def show_inventory(self):
        if not self.inventory:
            return "Your inventory is empty."
        return f"Inventory: {', '.join(self.inventory)}"


def start_game():
    grid = Grid(3)
    mapper = Map(grid)
    
    # Create player in starting room (0,0)
    starting_room = grid.rooms[(0, 0)]
    player = Player("Adventurer", starting_room)
    
    print(f"Welcome, {player.name}! You find yourself in a mysterious dungeon...")
    print("\nCurrent map of the dungeon:")
    mapper.render()
    print("You can use the following commands:")
    print("- move [direction] (north, south, east, west)")
    print("- use_door [room_id] (e.g., '(0, 1)')")
    print("- look")
    print("- investigate")
    print("- take [item]")
    print("- inventory")
    print("- quit")
    
    print("\n" + player.look_around())
    
    # Game loop
    while True:
        command = input("\nWhat would you like to do? ").strip().lower().split(" ", 1)
        
        if command[0] == "quit":
            print("Thanks for playing!")
            break
        
        elif command[0] == "move":
            if len(command) > 1:
                print(player.move_within_room(command[1]))
            else:
                print("Move where? Please specify a direction.")
        
        elif command[0] == "use_door":
            if len(command) > 1:
                try:
                    # Convert string representation of tuple to actual tuple
                    target = eval(command[1])
                    print(player.use_door(target))
                except:
                    print("Invalid room format. Use (row, col) format.")
            else:
                print("Which door? Please specify a room ID.")
        
        elif command[0] == "look":
            print(player.look_around())
        
        elif command[0] == "investigate":
            print(player.investigate())
        
        elif command[0] == "take":
            if len(command) > 1:
                print(player.take(command[1]))
            else:
                print("Take what? Please specify an item.")
        
        elif command[0] == "inventory":
            print(player.show_inventory())
        
        else:
            print("I don't understand that command.")


if __name__ == "__main__":
    start_game()