from roomTemplate import Room, Grid

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
        Grid(3,5)
        # Find and set the player's current room
        for room_obj in Room.all_rooms:
            if room_obj.id == starting_room_id:
                self.current_room = room_obj
                break
        self.current_room.add_cell_type("player", self.position[0], self.position[1])
    
    def move(self, direction):
        """
        Move the player in the specified direction (w, a, s, d)
        
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
        
        # Check if the new position is within the room bounds
        if 0 <= new_x < self.current_room.size and 0 <= new_y < self.current_room.size:
            # Update the player's position
            if self.check_for_door((new_x,new_y)):
                self.use_door((new_x,new_y))
                return True
            self.current_room.add_cell_type("none", *self.position)
            self.current_room.add_cell_type("player", new_x, new_y)
            self.position = (new_x, new_y)
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
    
    def use_door(self, sample_pos:tuple[int]|None = None):

        """
        Move through a door to the next room if standing on one
        
        Returns:
            bool: True if successfully moved to the next room, False otherwise
        """
        if sample_pos:
            door_info = self.check_for_door(sample_pos)
        else:
            door_info = self.check_for_door()
        if door_info:
            door_pos, target_room_id = door_info
            
            # Find the target room
            for room_obj in Room.all_rooms:
                if room_obj.id == target_room_id:
                    # Update the player's current room
                    self.current_room = room_obj
                    self.current_room_id = target_room_id
                    
                    # Determine entry position in the new room
                    # If exiting through north, enter through south, etc.
                    entry_positions = {
                        "north": "south",
                        "south": "north", 
                        "east": "west",
                        "west": "east"
                    }
                    
                    entry_pos = entry_positions[door_pos]
                    position_map = {
                        "north": (0, self.current_room.size//2),
                        "south": (self.current_room.size-1, self.current_room.size//2),
                        "east": (self.current_room.size//2, self.current_room.size-1),
                        "west": (self.current_room.size//2, 0)
                    }
                    
                    # Set the player's position to the entry door of the new room
                    self.position = position_map[entry_pos]
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


player = Player((0,1), (0, 2))
print(player.current_room.render_room())

while True:
    direction = input("Enter movement direction (w, a, s, d): ")
    if direction == "q":
        break
    if player.move(direction):
        print(player.current_room.render_room())
        print(player.get_position_info())
    elif player.use_door():
        print(player.current_room.render_room())
        print(player.get_position_info())
    else:
        print("Invalid move")