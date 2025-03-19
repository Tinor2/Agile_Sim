import time
from roomTemplate import Room, Grid
from all_puzzles import normal_puzzles as n_puzzles
import random
from readchar import readkey

class Player:
    def __init__(self, starting_room_id, starting_position):
        """
        Initialize a player with a starting room and position
        
        Args:
            starting_room_id: Tuple (row, col) identifying the starting room
            starting_position: Tuple (x, y) for starting coordinates within the room
        """
        self.current_room_id = starting_room_id
        self.position = starting_position
        self.current_room = None
        self.last_door_used = None  # Track last door used
        self.has_key = False  # Add this new attribute
        self.puzzles_solved = 0
        self.puzzles_required = 6  # Number of puzzles needed to unlock boss
        Grid(3,5)
        # Find and set the player's current room
        for room_obj in Room.all_rooms:
            if room_obj.id == starting_room_id:
                self.current_room = room_obj
                break
        self.current_room.add_cell_type("player", self.position[0], self.position[1])
    
    def move(self, direction):
        """
        Move the player in the specified direction (w, a, s, d). Also check for doors and special cells
        
        Args:
            direction: Character representing movement direction ('w', 'a', 's', 'd')
        
        Returns:
            bool: True if movement was successful, False otherwise
        """
        # Define direction mappings
        directions = {
            'w': (-1, 0),  # Up
            'a': (0, -1),  # Left
            's': (1, 0),   # Down
            'd': (0, 1)    # Right
        }
        
        if direction not in directions:
            return False
        
        # Calculate new position
        dx, dy = directions[direction]
        new_x, new_y = self.position[0] + dx, self.position[1] + dy
        use_old_pos = False
        # Check if the new position is within the room bounds
        if 0 <= new_x < self.current_room.size and 0 <= new_y < self.current_room.size:
            # Update the player's position
            if self.check_for_door((new_x,new_y)):
                self.use_door((new_x,new_y))
                return True
            if self.check_for_special_cell((new_x,new_y)):
                cell_type = self.check_for_special_cell((new_x,new_y))
                if cell_type == "locked":
                    if self.has_key:
                        # Transform locked cell into boss cell
                        self.current_room.cells[new_x][new_y] = Room.cell_icons["boss"]
                        print("\n🔓 The magical barrier transforms as your key resonates...")
                        time.sleep(1)
                        return False  # Don't move into the cell yet
                    else:
                        print("\n🔒 A magical barrier blocks your path. You need a special key...")
                        time.sleep(1)
                        return False
                elif cell_type == "boss":
                    # Handle boss encounter
                    print("\n⚔️ Preparing for boss battle...")
                    from all_puzzles import key_puzzles
                    if key_puzzles:
                        boss_puzzle = key_puzzles[0]  # Get the boss puzzle
                        result = boss_puzzle()
                        if result:
                            # Clear boss cell on victory
                            self.current_room.add_cell_type("none", new_x, new_y)
                            print("\n🎉 Boss defeated!")
                        else:
                            print("\n💔 Failed to defeat the boss...")
                        time.sleep(1)
                    return False
                if self.check_for_special_cell((new_x,new_y)) == "puzzle":
                    # Store original position
                    original_x, original_y = self.position
                    
                    # Clear screen before puzzle
                    print("\033[H\033[J", end="")
                    print("\n" + "="*50)
                    print("📜 Eldrin discovers an ancient puzzle!")
                    print("="*50 + "\n")
                    time.sleep(1)  # Pause for dramatic effect
                    
                    random_puzzle = random.choice(n_puzzles)
                    result = random_puzzle()
                    
                    # Only remove puzzle from pool and clear tile if solved
                    if result:
                        self.puzzles_solved += 1  # Increment solved puzzles
                        
                        # Check if boss room should be unlocked
                        if self.puzzles_solved >= self.puzzles_required:
                            self.has_key = True
                            print("\n🗝️  With this puzzle solved, you now have enough knowledge to challenge the boss!")
                            print(f"Puzzles solved: {self.puzzles_solved}/{self.puzzles_required}")
                        else:
                            print(f"\n📊 Puzzles solved: {self.puzzles_solved}/{self.puzzles_required}")
                        
                        # Move to puzzle tile position
                        self.current_room.add_cell_type("none", *self.position)
                        self.current_room.add_cell_type("player", new_x, new_y)
                        self.position = (new_x, new_y)
                        print("\n✨ Puzzle solved successfully!")
                    else:
                        # Stay at original position if puzzle failed
                        print("\n❌ Puzzle not solved. The magical barrier remains...")
                        self.position = (original_x, original_y)
                        time.sleep(1)
                        use_old_pos = True
                    # Pause after puzzle attempt
                    input("\nPress Enter to continue...")
                    
                    # Clear screen and return to game
                    print("\033[H\033[J", end="")
                    print("\n" + "="*50)
                    print("Returning to exploration...")
                    print("="*50 + "\n")
                    time.sleep(1)
            self.current_room.add_cell_type("none", *self.position)
            if not use_old_pos:
                self.current_room.add_cell_type("player", new_x, new_y)
                self.position = (new_x, new_y)
            else:
                self.current_room.add_cell_type("player", original_x, original_y)
                use_old_pos = False
            return True
        return False
    
    def check_for_door(self, sample_pos:tuple[int]|None = None):
        """
        Check if the player is standing on a door tile
        
        Returns:
        tuple or None: (door_position, target_room_id) if on a door, None otherwise
        """
        if sample_pos:
            x,y = sample_pos
            print("using new position")
        else:    
            print("using not new position")
            x, y = self.position
        print(f"PLAYER POS: {x, y} CURRENT TILE: {self.current_room.cells[x][y]}")
        if self.current_room.cells[x][y] == Room.cell_icons["door"]:
            # Find which door this is
            for door_pos, target_room_id in self.current_room.doors:
                # Map string positions to grid coordinates
                position_map = {
                    "north": (0, self.current_room.size//2),
                    "south": (self.current_room.size-1, self.current_room.size//2),
                    "east": (self.current_room.size//2, self.current_room.size-1),
                    "west": (self.current_room.size//2, 0)
                }
                door_x, door_y = position_map[door_pos]
                
                if (door_x, door_y) == (x, y):
                    return door_pos, target_room_id
        return None
    def check_for_special_cell(self, sample_pos:tuple[int]|None = None):
        """
        Check if the player is standing on a special cell, other than doorways
        
        Returns:
        str or None: Special cell type if on one, None otherwise
        """
        if sample_pos:
            x, y = sample_pos
        else:
            x, y = self.position
        for cell_type, icon in Room.cell_icons.items():
            if icon == self.current_room.cells[x][y] and cell_type != "door":
                return cell_type
        return None

    def use_door(self, sample_pos:tuple[int]|None = None):
        """
        Move through a door to the next room and place player one cell in front of the door
        
        Returns:
            bool: True if successfully moved to the next room, False otherwise
        """
        if sample_pos:
            door_info = self.check_for_door(sample_pos)
        else:
            door_info = self.check_for_door()
        if door_info:
            door_pos, target_room_id = door_info
            entry_positions = {
                "north": "south", 
                "south": "north",
                "east": "west",
                "west": "east"
            }
            self.last_door_used = entry_positions[door_pos]  # Store the entry direction
            
            # Find the target room
            for room_obj in Room.all_rooms:
                if room_obj.id == target_room_id:
                    # Update the player's current room
                    self.current_room = room_obj
                    self.current_room_id = target_room_id
                    
                    # Determine entry position in the new room
                    position_map = {
                        "north": (0, self.current_room.size//2),
                        "south": (self.current_room.size-1, self.current_room.size//2),
                        "east": (self.current_room.size//2, self.current_room.size-1),
                        "west": (self.current_room.size//2, 0)
                    }
                    
                    # Get the door position
                    door_x, door_y = position_map[entry_positions[door_pos]]
                    
                    # Calculate position one cell in front of the door
                    offset_map = {
                        "north": (1, 0),    # Move one cell down from north door
                        "south": (-1, 0),   # Move one cell up from south door
                        "east": (0, -1),    # Move one cell left from east door
                        "west": (0, 1)      # Move one cell right from west door
                    }
                    
                    offset_x, offset_y = offset_map[entry_positions[door_pos]]
                    self.position = (door_x + offset_x, door_y + offset_y)
                    
                    # Clear any previous player position and set the new one
                    self.current_room.add_cell_type("player", *self.position)
                    return True
            return False
        return False
    
    def get_position_info(self):
        """
        Get information about the player's current position
        
        Returns:
            dict: Information including room ID and position
        """
        return {
            "room_id": self.current_room_id,
            "position": self.position,
        }

def main():
    # Initialize player
    player = Player((0,1), (0, 2))
    print(player.current_room.render_room())
    print("Use WASD to move, Q to quit")
    
    # Main game loop
    try:
        while True:
            key = readkey()
            if key in ['w', 'a', 's', 'd']:
                handle_movement(player, key)
            elif key == 'q':
                print("\nExiting game...")
                break
    except KeyboardInterrupt:
        print("\nGame terminated by user")

def handle_movement(player, direction):
    old_room_id = player.current_room_id
    if player.move(direction):
        print("\033[H\033[J", end="")  # Clear screen
        # If room changed, show transition message
        if old_room_id != player.current_room_id:
            print("\n" + "="*50)
            print(f"🚪 Moving from Room {old_room_id} to Room {player.current_room_id}")
            print(f"Entering through the {player.last_door_used} door")
            print("="*50 + "\n")
        else:
            print("\n" + "="*50)
            print(f"Currently in {old_room_id}...")
            print("="*50 + "\n\n")
        
        print(player.current_room.render_room())
        print(f"\n📍 Current Position: {player.get_position_info()}")
        print("\n🎮 Controls: WASD to move, Q to quit")
    time.sleep(0.2)

if __name__ == "__main__":
    main()