from visu import plot_path
import sys
import copy


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
            )
        

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
        print(f"{lines}")

        try:
            map_to_return.width = len(lines[0])
        except IndexError: #not very beautiful, but if index zero is not there, its empty
            map_to_return.width = 0
        map_to_return.height = len(lines)  
        if end is not None:
            map_to_return.set_end(end[0], end[1])
        if start is not None:
            map_to_return.set_start(start[0], start[1])

        return map_to_return

class Walker:
    # Walker class represents a walker with a position on the map
    def __init__(self, position_information):
        # Initialize the walker's position from field or get from the map
        if isinstance(position_information, Map):
            self.position = position_information.start
        elif isinstance(position_information, Field): 
            self.position = position_information

    def can_climb(self, field):
        if self.position.elevation + 1 == field.elevation:
            return True
        elif self.position.elevation >= field.elevation:
            return True
        return False
    
    def count_climbable_neighbors(self, neigbors):
        #neigbors comes in tuple NSWE
        (n, s, w, e) = neigbors
        count = 0
        if self.can_climb(n):
            count += 1
        if self.can_climb(s):
            count += 1
        if self.can_climb(w):
            count += 1
        if self.can_climb(e):
            count += 1
        return count
        


class Path:
    # Path class represents a sequence of fields forming a path on the map
    def __init__(self, walker=None):
        # Initialize an empty list of fields
        self.fields = []
        # If creation with walker, add start to fields
        if isinstance(walker, Walker):
            self.fields.append(walker.position)

    def add_step(self, field: Field):
        # Add a new step to the path
        self.fields.append(field)

    def remove_last_step(self):
        # Remove the last step from the path
        if self.fields:
            self.fields.pop()

    def get_length(self):
        return len(self.fields)
    
    def get_end(self) -> Field:
        if not self.fields:
            return None
        return self.fields[len(self.fields) - 1]
    
    def field_visited(self, field) -> bool:
        for f in self.fields:
            if f == field:
                return True
        return False
 


class ShortestPathFinder:

    @staticmethod
    def solve(map: Map, path: Path, walker: Walker) -> Path:
        if walker.position == map.end:
            return copy.deepcopy(path)
        
        shortest_path = None

        for neigbor in map.get_neighbours(walker.position):
            if walker.can_climb(neigbor) and not path.field_visited(neigbor):
                walker.position = neigbor
                path.add_step(walker.position)
                
                found_path = ShortestPathFinder.solve(map, path, walker)
                
                path.remove_last_step()
                
                if shortest_path is None:
                    shortest_path = found_path  
                elif found_path and found_path.get_length() < shortest_path.get_length():
                    shortest_path = found_path
                    
        return shortest_path 


    
if __name__ == '__main__':

    # GIVEN a mutli line string with a full map 
    map_string = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""";

    world = Map.from_string(map_string)
    walker = Walker(world)
    path = Path(walker)

    # THEN the path length should be 31 and the ending field 2, 5, 25
    shortest = ShortestPathFinder.solve(world, path, walker)
    plot_path(shortest.fields, 5, 8)
