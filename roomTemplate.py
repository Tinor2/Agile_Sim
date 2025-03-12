class room():
    all_rooms = []
    def __init__(self,id, size):
        room.all_rooms.append(self)
        self.id = id
        doors = []
        for component in range(2): # for each coordinate
            for multi in [-1,1]: # plus or minus multiplier, first coordinate
                shifted_coord = self.id[component]+multi
                if shifted_coord >=0 and shifted_coord < size: # if the neighbor is within the grid
                    doors.append((shifted_coord,self.id[1]))
        for multi in [-1,1]: # plus or minus multiplier, for the first coordinate
            shifted_coord = self.id[1]+multi
            if self.id[1]+multi >=0 and self.id[1]+multi < size: # if the neighbor is within the grid
                doors.append((self.id[1],self.id[0]+multi)) # plus or minus multiplier, for the second coordinate
        self.doors = doors
class init_grid():
    def __init__(self, grid_size:int,room_size:int):
        self.size = grid_size
        self.room_size = room_size
        pass
    def defineRooms(self):
        grid_rooms = []
        for row in range(self.size): # Create a room for each cell in a grid
            for col in range(self.size):
                grid_rooms.append(room((row,col),self.room_size))
                print(grid_rooms[-1].doors)
        return grid_rooms


init_grid(2,3).defineRooms()