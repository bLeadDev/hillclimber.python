from visu import plot_path

def get_elevation_from_char(elevation_char):
    if elevation_char == 'S':
        return 0
    elif elevation_char == 'E':
        return 25
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
        return self.fields[(x,y)]

    def get_neighbours(self, field):
        # Get a list of available neighbouring fields (N, S, W, E) of the given field
        # if they are not on the map, they are not available

        if field.x > self.width - 1 or field.y > self.height - 1:
            return None #outside of range
        
        neighbouring_fields = (None, None, None, None)

        if field.y != 0:          #add north
            neighbouring_fields = (
                self.fields[(field.x, field.y - 1)],
                neighbouring_fields[1],
                neighbouring_fields[2],
                neighbouring_fields[3]
            )

        if field.y != self.height - 1: #add south
            neighbouring_fields = (
                neighbouring_fields[0],
                self.fields[(field.x, field.y + 1)],
                neighbouring_fields[2],
                neighbouring_fields[3]
            )

        if field.x != 0:          #add east
            neighbouring_fields = (
                neighbouring_fields[0],
                neighbouring_fields[1],
                self.fields[(field.x - 1, field.y)],
                neighbouring_fields[3]
            )
        if field.x != self.width - 1:          #add west
            neighbouring_fields = (
                neighbouring_fields[0],
                neighbouring_fields[1],
                neighbouring_fields[2],
                self.fields[(field.x + 1, field.y)],
            )
 
        return neighbouring_fields
        

    @staticmethod
    def from_string(map_string: str):
        # Static method to create a Map object from a multiline string
        start = None
        end = None
        map_to_return = Map()
        lines = map_string.splitlines()
        for idx_y, line in enumerate(lines):
            for idx_x, ch in enumerate(line):
                #search for start and end. As specified, start has elevation of a and end z
                if ch == 'S':
                    start = (idx_x, idx_y)
                    ch = 'a'
                elif ch == 'E':
                    end = (idx_x, idx_y)
                    ch = 'z'
                map_to_return.add_field(x=idx_x, y=idx_y, elevation=get_elevation_from_char(ch))
        if end is not None:
            map_to_return.set_end(end[0], end[1])
        if start is not None:
            map_to_return.set_start(start[0], start[1])
        map_to_return.width = idx_x + 1
        map_to_return.height = idx_y + 1
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
    found_paths = []

    @staticmethod
    def solve(map: Map, path: Path, walker: Walker):
        if walker.position == map.end:
            path.add_step(walker.position)
            return path
        
        neighbors = map.get_neighbours(walker.position)
        # Initialize shortest path variable
        current_path = None
        shortest_path = None

        for neighbor in neighbors:
            if neighbor is not None and not path.field_visited(neighbor) and walker.can_climb(neighbor):
                walker.position = neighbor
                path.add_step(neighbor)
                current_path = ShortestPathFinder.solve(map, path, walker)
                path.remove_last_step()

            if current_path is not None:
                if map.end == current_path.get_end():
                    print(f"map end is: {map.end}\ncurrent end{current_path.get_end()}")
                    print(f"current path: {current_path.fields}")
                    ShortestPathFinder.found_paths.append(current_path)
                    plot_path(current_path.fields, map.height, map.width)
                    # if (shortest_path is None or current_path.get_length() < shortest_path.get_length()):
                    #     shortest_path = current_path
                    #     print("New shortest path: {}", shortest_path.get_length())
                    #     print(f"h:{map.height}, w: {map.width}")
                    #     plot_path(shortest_path.fields, map.height, map.width)
        
        return  shortest_path


# Rest of your code remains unchanged


map_string = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

w = Walker(Field(x=0, y=0,elevation=0))
m = Map.from_string(map_string=map_string)


p = Path()
p.add_step(w.position) #should be done in the class/method
shortest = ShortestPathFinder.solve(m, p, w)




multilinestring = """\
abc
def
ghi"""

print(multilinestring)