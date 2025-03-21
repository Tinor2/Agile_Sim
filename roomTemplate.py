import json
import random

class Room:
    all_rooms = []
    # Load cell icons from JSON file
    with open('cell_icons.json', 'r') as f:
        cell_icons = json.load(f)

    def __init__(self, id, grid_size):
        self.id = id
        self.doors = []
        self.size = grid_size
        self.cells = [[Room.cell_icons["none"] for _ in range(grid_size)] for _ in range(grid_size)]
        Room.all_rooms.append(self)
        self.has_player = False
        self.puzzle_count = 0  # Add puzzle counter
        self.max_puzzles = 2   # Set maximum puzzles per room
    def add_door(self, door_position, target_room_id):
        self.doors.append((door_position, target_room_id))
        # Map string positions to grid coordinates
        position_map = {
            "north": (0, self.size//2),
            "south": (self.size-1, self.size//2),
            "east": (self.size//2, self.size-1),
            "west": (self.size//2, 0)
        }
        x, y = position_map[door_position]
        self.cells[x][y] = Room.cell_icons["door"]
    def add_cell_type(self, cell_type, x, y):
        if Room.cell_icons.get(cell_type) is None:
            raise ValueError(f"Invalid cell type: {cell_type}")
        # Allow locked and boss cells to be added
        if cell_type in ["locked", "boss"]:
            self.cells[x][y] = Room.cell_icons[cell_type]
            return True
        if cell_type == "puzzle":
            if self.puzzle_count >= self.max_puzzles:
                return False
            self.puzzle_count += 1
        if cell_type == "player":
            if self.has_player:
                # Clear any existing player icon
                self.clear_player()
            self.has_player = True
        self.cells[x][y] = Room.cell_icons[cell_type]
        return True
    
    def clear_player(self):
        """Remove player icon from room"""
        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y] == Room.cell_icons["player"]:
                    self.cells[x][y] = Room.cell_icons["none"]
        self.has_player = False

    def render_room(self, ):
        display = ""
        # Print top border
        display += "+" + "---+" * self.size + "\n"
        
        # Print rows
        for row in range(self.size):
            # Cell content
            cell_line = "|"
            for col in range(self.size):
                cell_content = self.cells[row][col]
                cell_line += f" {cell_content} |"
            display += cell_line + "\n"
            
            # Bottom border for each row
            display += "+" + "---+" * self.size + "\n"
        return display

class Grid:
    def __init__(self, grid_size:int, room_size:int|None=None, boss_room:bool|None=None):
        if room_size is None:
            room_size = 3
        elif room_size % 2 == 0:
            raise ValueError("Room size must be an odd number") 
        if boss_room is None:
            boss_room = True
        self.room_size = room_size
        self.size = grid_size
        self.rooms = {}
        self.boss_room = boss_room
        self.define_rooms()
        self.connect_rooms()
        self.add_puzzles(10, is_center=True)
    
    def define_rooms(self):
        # Create rooms in a grid pattern
        for row in range(self.size):
            for col in range(self.size):
                room_id = (row, col)
                self.rooms[room_id] = Room(room_id, self.room_size)
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
    def add_puzzles(self, total_puzzles:int, is_center:bool|None = None):
        if is_center is None:
            is_center = False
        puzzles_added = 0
        max_attempts = total_puzzles * 3  # Prevent infinite loops
        attempts = 0

        while puzzles_added < total_puzzles and attempts < max_attempts:
            room = random.choice(Room.all_rooms)
            attempts += 1

            # Skip center room if is_center is True
            if is_center and room.id == (self.size//2, self.size//2):
                continue

            # Skip if room has reached max puzzles
            if room.puzzle_count >= room.max_puzzles:
                continue

            x = random.randint(0, room.size-1)
            y = random.randint(0, room.size-1)

            if room.cells[x][y] == Room.cell_icons["none"]:
                if room.add_cell_type("puzzle", x, y):
                    puzzles_added += 1
                    # print(f"Added puzzle {puzzles_added} to room {room.id}")
        if self.boss_room:
            # Add boss puzzle to center room
            center_room = self.rooms[(self.size//2, self.size//2)]
            center_room.add_cell_type("locked", center_room.size//2, center_room.size//2)
            # print("Added boss puzzle to center room")
    def print_grid(self):
        for row in range(self.size):
            for col in range(self.size):
                room = self.rooms[(row, col)]
                render_room_cells = ""
                print(f"Room {room.id} has {len(room.doors)} doors connecting to: {[target for _, target in room.doors]} and with a layout of \n{room.render_room()}")
                
class Map:
    def __init__(self, grid):
        self.grid = grid
    
    def render(self):
        size = self.grid.size
        door_icon = "D"
        # Create the top border row
        top_row = "+"
        for col in range(size):
            room = self.grid.rooms[(0, col)]
            if any(door_pos == "north" for door_pos, _ in room.doors):
                top_row += f"----{door_icon}---+"
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
                            lines[i] += door_icon
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
                    lines[1] += door_icon
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
                        sep_row += f"----{door_icon}---+"
                    else:
                        sep_row += "--------+"
                print(sep_row)
        
        # Create the bottom border row
        bottom_row = "+"
        for col in range(size):
            room = self.grid.rooms[(size-1, col)]
            if any(door_pos == "south" for door_pos, _ in room.doors):
                bottom_row += f"----{door_icon}---+"
            else:
                bottom_row += "--------+"
        print(bottom_row)


def demo(size=3):
    """Create a grid of the specified size and render it"""
    print(f"Creating a {size}x{size} grid of rooms:")
    grid = Grid(size,5)
    # grid.add_puzzles(10,True)
    mapper = Map(grid)
    print("\nRoom Information:")
    grid.print_grid()
    print("\nRoom Grid Map:")
    mapper.render()
    # Print a specific room with ID (0,0)
    print("\nRendering room (1,1):")
    print(grid.rooms[(1,1)].render_room())
 
# Run a demo with a 3x3 grid
if __name__ == "__main__":
    demo(3)