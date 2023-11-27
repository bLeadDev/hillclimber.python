#from visu import plot_path
import sys

def get_elevation_from_char(elevation_char, coord):
    if elevation_char == 'S':
        return 0
    elif elevation_char == 'E':
        return 25
    elif ord(elevation_char) > ord('z') or ord(elevation_char) < ord('a'):
        raise Exception(f"Invalid cell detected at {coord}!")
    else:
        return ord(elevation_char) - ord('a')

class Field:
    # Field class represents a single field on the map
    def __init__(self, x, y, elevation):
        # Initialize the field's position and elevation
        self.x = x
        self.y = y
        self.elevation = elevation

    def __repr__(self):
        # Return a string representation of the field
        return f'Field(x={self.x}, y={self.y}, elevation={self.elevation})'

    def __eq__(self, other):
        # Return True if the fields are equal, False otherwise
        return self.x == other.x and self.y == other.y and self.elevation == other.elevation

class Map:
    # Map class represents a 2D map of fields
    def __init__(self):
        # Initialize an empty list of fields
        self.fields = {}
        self.width = 0
        self.height = 0

    def set_start(self, x, y):
        # Set the start field at given x, y coordinates
        # dont forget to make sure that this field was added to the map prior
        # to calling this method (otherwise you will get a KeyError)
        self.start = self.get_field(x, y)

    def set_end(self, x, y):
        # Set the end field at given x, y coordinates
        # dont forget to make sure that this field was added to the map prior
        # to calling this method (otherwise you will get a KeyError)
        self.end = self.get_field(x, y)

    def add_field(self, x, y, elevation):
        # Add a new field to the map with given x, y coordinates and elevation
        self.fields[(x,y)] = Field(x, y, elevation)

    def get_field(self, x, y):
        # Get the field at given x, y coordinates
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return Field(x, y, sys.maxsize)
        return self.fields[(x,y)]

    def get_neighbours(self, field):
        # Get a list of available neighbouring fields (N, S, W, E) of the given field
        # if they are not on the map, they are not available

        return (
                self.get_field(field.x + 0, field.y - 1),
                self.get_field(field.x + 0, field.y + 1),
                self.get_field(field.x - 1, field.y + 0),
                self.get_field(field.x + 1, field.y + 0)
            );
        

    @staticmethod
    def from_string(map_string: str):
        # Static method to create a Map object from a multiline string
        start = None
        end = None
        map_to_return = Map()
        lines = map_string.splitlines()
        idx_x = -1
        idx_y = -1
        for idx_y, line in enumerate(lines):
            for idx_x, ch in enumerate(line):
                #search for start and end. As specified, start has elevation of a and end z
                if ch == 'S':
                    if start is not None:
                        raise Exception("Multiple starting points detected!")
                    start = (idx_x, idx_y)
                    ch = 'a'
                elif ch == 'E':
                    if end is not None:
                        raise Exception("Multiple ending points detected!")
                    end = (idx_x, idx_y)
                    ch = 'z'
                map_to_return.add_field(x=idx_x, y=idx_y, elevation=get_elevation_from_char(ch, (idx_x, idx_y)))
        map_to_return.width = len(lines[0])
        map_to_return.height = len(lines)  
        if end is not None:
            map_to_return.set_end(end[0], end[1])
        if start is not None:
            map_to_return.set_start(start[0], start[1])

        return map_to_return

class Walker:
    # Walker class represents a walker with a position on the map
    def __init__(self, position: Field):
        # Initialize the walker's position
        self.position = position

    def can_climb(self, field):
        if self.position.elevation + 1 == field.elevation:
            return True
        elif self.position.elevation >= field.elevation:
            return True
        return False
        


class Path:
    # Path class represents a sequence of fields forming a path on the map
    def __init__(self):
        # Initialize an empty list of fields
        self.fields = []

    def add_step(self, field):
        # Add a new step to the path
        self.fields.append(field)

    def remove_last_step(self):
        # Remove the last step from the path
        if self.fields:
            self.fields.pop()

    def get_length(self):
        return len(self.fields)
    
    def get_end(self):
        return self.fields[len(self.fields) - 1]
    
    def field_visited(self, field):
        for f in self.fields:
            if f == field:
                return True
        return False
 


class ShortestPathFinder:
    def __init__(self):
        self.shortest_path = None
        self.found_paths = []

    def get_shortest(self):
        shortest = self.found_paths[0] 
        for f in self.found_paths:
            if f.get_length() < shortest.get_length():
                shortest = f
            print(f.fields)
        self.shortest_path = shortest
        

    def solve(self, map: Map, path: Path, walker: Walker):
        path.add_step(walker.position)

        if map.end == walker.position:
            return path
        
        current_path = None

        for neighbor in map.get_neighbours(walker.position):
            if neighbor is not None and not path.field_visited(neighbor) and walker.can_climb(neighbor):
                walker.position = neighbor
                current_path = self.solve(map=map, path=path, walker=walker)
                if current_path is not None:
                    self.found_paths.append(current_path)

# Rest of your code remains unchanged

if __name__ == '__main__':
    map_string = """\
abda
abcd"""
    w = Walker(Field(0, 0, 0))
    p = Path()
    # WHEN creating a map from the string, setting the end and solve
    world = Map.from_string(map_string)
    world.set_end(3, 0)
    
    # THEN the path should be one of the following two 
    shortest = ShortestPathFinder.solve(world, p, w)

    map_string = """\
    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi"""



