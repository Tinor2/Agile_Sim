class room:
    all_rooms = []
    
    def __init__(self, id, grid_size):
        self.id = id
        self.doors = []  # Will contain tuples of (door_position, target_room_id)
        room.all_rooms.append(self)
    
    def add_door(self, door_position, target_room_id):
        self.doors.append((door_position, target_room_id))
    
    def __repr__(self):
        return f"Room {self.id} with doors to {[target for _, target in self.doors]}"


class Grid:
    def __init__(self, grid_size):
        self.size = grid_size
        self.rooms = {}
        self.define_rooms()
        self.connect_rooms()
    
    def define_rooms(self):
        # Create rooms in a grid pattern
        for row in range(self.size):
            for col in range(self.size):
                room_id = (row, col)
                self.rooms[room_id] = room(room_id, self.size)
        return self.rooms
    def connect_rooms(self):
        # Define possible directions: North, East, South, West
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        door_positions = ["north", "east", "south", "west"]
        
        for room_id, room in self.rooms.items():
            row, col = room_id
            
            # Check each direction
            for direction_idx, (dr, dc) in enumerate(directions):
                neighbor_row, neighbor_col = row + dr, col + dc
                neighbor_id = (neighbor_row, neighbor_col)
                
                # Check if neighbor exists
                if 0 <= neighbor_row < self.size and 0 <= neighbor_col < self.size:
                    door_position = door_positions[direction_idx]
                    room.add_door(door_position, neighbor_id)
    
    def print_grid(self):
        for row in range(self.size):
            for col in range(self.size):
                room = self.rooms[(row, col)]
                print(f"Room {room.id} has {len(room.doors)} doors connecting to: {[target for _, target in room.doors]}")


class Map:
    def __init__(self, grid):
        self.grid = grid
    
    def render(self):
        """Render the grid with perfectly aligned borders and doors"""
        size = self.grid.size
        
        # Create the top border row
        top_row = "+"
        for col in range(size):
            room = self.grid.rooms[(0, col)]
            if any(door_pos == "north" for door_pos, _ in room.doors):
                top_row += "----D---+"
            else:
                top_row += "--------+"
        print(top_row)
        
        # For each row of rooms
        for row in range(size):
            # Create three lines for each room row (top, middle with ID, bottom)
            lines = ["", "", ""]
            # Build each line across all columns
            for col in range(size):
                room = self.grid.rooms[(row, col)]
                
                # Left wall or door (west)
                has_west_door = any(door_pos == "west" for door_pos, _ in room.doors)
                
                # Only add the left border for the first column or if there's no door
                if col == 0 or not has_west_door:
                    for i in range(3):
                        if i == 1 and has_west_door and col > 0:
                            lines[i] += "D"
                        else:
                            lines[i] += "|"
                
                # Room content
                lines[0] += "        "  # 8 spaces
                
                # Room ID in the middle line
                room_id = f" {row},{col} "
                padding = 8 - len(room_id)
                left_pad = padding // 2
                right_pad = padding - left_pad
                lines[1] += " " * left_pad + room_id + " " * right_pad
                
                lines[2] += "        "  # 8 spaces
                
                # Right wall or door (east)
                if any(door_pos == "east" for door_pos, _ in room.doors):
                    lines[1] += "D"
                    lines[0] += "|"
                    lines[2] += "|"
                else:
                    lines[0] += "|"
                    lines[1] += "|"
                    lines[2] += "|"
            
            # Print the three lines for this row
            for line in lines:
                print(line)
            
            # Bottom border for this row
            if row < size - 1:
                # Create the separator row with south/north doors
                sep_row = "+"
                for col in range(size):
                    room = self.grid.rooms[(row, col)]
                    if any(door_pos == "south" for door_pos, _ in room.doors):
                        sep_row += "----D---+"
                    else:
                        sep_row += "--------+"
                print(sep_row)
        
        # Create the bottom border row
        bottom_row = "+"
        for col in range(size):
            room = self.grid.rooms[(size-1, col)]
            if any(door_pos == "south" for door_pos, _ in room.doors):
                bottom_row += "----D---+"
            else:
                bottom_row += "--------+"
        print(bottom_row)


def demo(size=3):
    """Create a grid of the specified size and render it"""
    print(f"Creating a {size}x{size} grid of rooms:")
    grid = Grid(size)
    mapper = Map(grid)
    print("\nRoom Information:")
    grid.print_grid()
    print("\nRoom Grid Map:")
    mapper.render()

# Run a demo with a 3x3 grid
if __name__ == "__main__":
    demo(4)