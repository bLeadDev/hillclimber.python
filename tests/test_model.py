
import pytest
from src.model import Map, Field, Walker, Path, ShortestPathFinder, get_elevation_from_char
#############################
#
# SOLVING TESTS
# 
#############################
def test_solving_a_single_line_map():
    # GIVEN a single line string, an empty path and a walker at pos 0, 0
    map_string = """\
ab"""
    w = Walker(Field(0, 0, 0))
    p = Path()
    # WHEN creating a map from the string, setting the end and solve
    world = Map.from_string(map_string)
    world.set_end(1, 0)
    
    # THEN the path should find the path (0, 0), (0, 1)
    spf = ShortestPathFinder()
    spf.solve(world, p, w) 
    spf.get_shortest()
    shortest = spf.shortest_path
    assert shortest.fields == [Field(0, 0, 0), Field(1, 0, 1)]

@pytest.mark.skip(reason="WIP")
def test_solving_a_multi_line_map():

    # GIVEN a single line string, an empty path and a walker at pos 0, 0
    map_string = """\
abda
abcd"""
    w = Walker(Field(0, 0, 0))
    p = Path()
    # WHEN creating a map from the string, setting the end and solve
    world = Map.from_string(map_string)
    world.set_end(3, 0)
    
    # THEN the path length should be 5 
    spf = ShortestPathFinder()
    spf.solve(world, p, w) 
    spf.get_shortest()
    shortest = spf.shortest_path    
    assert shortest.get_length() == 5




#############################
#
# WALKER TESTS
# 
#############################

def test_create_a_walker_who_is_able_to_climb_one_up():
    # GIVEN a walker at random position, elevation 0
    walker = Walker(Field(x=0, y=0, elevation=0))
    # WHEN trying to climb a field with elevation 1
    # THEN the climber should be able to climb it
    assert(walker.can_climb(Field(x=1, y=0, elevation=1)) == True)

def test_create_a_walker_who_is_able_to_climb_down():
    # GIVEN a walker at random position, elevation 15
    walker = Walker(Field(x=0, y=0, elevation=15))
    # WHEN trying to climb a field with elevation 1
    # THEN the climber should be able to climb down to it
    assert(walker.can_climb(Field(x=1, y=0, elevation=1)) == True)

def test_create_a_walker_who_is_not_able_to_climb_up_more_than_one():
    # GIVEN a walker at random position, elevation 0
    walker = Walker(Field(x=0, y=0, elevation=0))
    # WHEN trying to climb a field with elevation 2
    # THEN the climber should NOT be able to climb up
    assert(walker.can_climb(Field(x=1, y=0, elevation=2)) == False)

#############################
#
# MAP AND FIELD TESTS
# 
#############################

def test_add_a_field_to_a_map():
    # GIVEN an empty map
    world = Map()
    # WHEN adding a new field (x=0, y=0, elevation 5)
    world.add_field(0, 0, 5)

    # THEN the map should contain a field with elevation 5 at (x=0, y=0)
    assert world.get_field(0, 0) == Field(0, 0, 5)

def test_adding_multiple_fields_to_a_map():
    # GIVEN an empty map
    world = Map()
    # WHEN adding a new field (x=0, y=0, elevation 5)
    world.add_field(0, 0, 5)
    # AND adding a new field (x=1, y=0, elevation 3)
    world.add_field(1, 0, 3)

    # THEN the map should contain a field with elevation 5 at (x=0, y=0)
    assert world.get_field(0, 0) == Field(0, 0, 5)

    # AND the map should contain a field with elevation 3 at (x=1, y=0)
    assert world.get_field(1, 0) == Field(1, 0, 3)

def test_create_a_simple_oneline_map_from_string():
    # GIVEN a multiline string
    map_string = """\
ab"""
    # WHEN creating a map from the string
    world = Map.from_string(map_string)
    # THEN the map should contain a field with elevation 0 (=a) at (x=0, y=0)
    assert world.get_field(0, 0) == Field(0, 0, 0)
    # AND the map should contain a field with elevation 1 (=b) at (x=1, y=0)
    assert world.get_field(1, 0) == Field(1, 0, 1)

def test_create_a_simple_twoline_map_from_string():
    # GIVEN a multiline string
    map_string = """\
a
b"""
    # WHEN creating a map from the string
    world = Map.from_string(map_string)
    # THEN the map should contain a field with elevation 0 (=a) at (x=0, y=0)
    assert world.get_field(0, 0) == Field(0, 0, 0)
    # AND the map should contain a field with elevation 1 (=b) at (x=0, y=1)
    assert world.get_field(0, 1) == Field(0, 1, 1)

def test_create_a_minimal_complex_twoline_map_from_string():
    # GIVEN a multiline string
    map_string = """\
abbc
bbaa
caac"""
    # WHEN creating a map from the string
    world = Map.from_string(map_string)
    # THEN the map should contain all fields with with the given elevation
    assert world.get_field(0, 0) == Field(x=0, y=0, elevation=0)
    assert world.get_field(0, 1) == Field(x=0, y=1, elevation=1)
    assert world.get_field(0, 2) == Field(x=0, y=2, elevation=2)
    assert world.get_field(1, 0) == Field(x=1, y=0, elevation=1)
    assert world.get_field(1, 1) == Field(x=1, y=1, elevation=1)
    assert world.get_field(1, 2) == Field(x=1, y=2, elevation=0)
    assert world.get_field(2, 0) == Field(x=2, y=0, elevation=1)
    assert world.get_field(2, 1) == Field(x=2, y=1, elevation=0)
    assert world.get_field(2, 2) == Field(x=2, y=2, elevation=0)
    assert world.get_field(3, 0) == Field(x=3, y=0, elevation=2)
    assert world.get_field(3, 1) == Field(x=3, y=1, elevation=0)
    assert world.get_field(3, 2) == Field(x=3, y=2, elevation=2)


def test_create_a_map_with_start_and_end():
    # GIVEN a multiline string with start and end
    map_string = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    # WHEN creating a map from the string
    world = Map.from_string(map_string)
    # THEN the map should have the right starting and ending point, with elevation 0 at S and 25 at E
    assert world.start  == Field(x=0, y=0, elevation=0)
    assert world.end    == Field(x=5, y=2, elevation=25)

def test_create_a_map_with_multiple_starts_and_one_end():
    # GIVEN a multiline string with multiple starts and one end
    map_string = """\
Sabqponm
abcryxxl
accszExk
Scctuvwj
abdefghi"""
    # WHEN creating a map with multiple starting points
    try:
        world = Map.from_string(map_string)
        works = False
    except:
        works = True
        # THEN the map should throw an error that indicates too many starting points

    assert works == True

    



def test_create_a_map_with_one_start_and_multiple_ends():
    # GIVEN a multiline string with multiple starts and one end
    map_string = """\
Sabqponm
abcryxEl
accszExk
acctuvwj
abdefghi"""
    # WHEN creating a map with multiple end points
    # THEN the map should throw an error that indicates too many end points

    with pytest.raises(Exception) as excinfo:
        world = Map.from_string(map_string)
    assert str(excinfo.value) == "Multiple ending points detected!"

def test_create_a_map_with_invalid_cell():
    # GIVEN a multiline string with start and end
    map_string = """\
a.mmlxl"""
    # WHEN creating a map from the string
    with pytest.raises(Exception) as excinfo:
        world = Map.from_string(map_string)
    assert str(excinfo.value) == "Invalid cell detected at (1, 0)!"

def test_get_neightbors_in_middle():
    # GIVEN a multiline string with start and end
    map_string = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    world = Map.from_string(map_string)
    # WHEN trying to get the neighboring fields
    neighbor = world.get_neighbours(Field(x=2, y=2, elevation=2))
    # THEN the map should return the right neighbors (N, S, W, E)
    assert neighbor == (
        Field(x=2, y=1, elevation=2), #north
        Field(x=2, y=3, elevation=2), #south
        Field(x=1, y=2, elevation=2), #west
        Field(x=3, y=2, elevation=18) #east
    )

def test_get_neightbors_at_edge_x0_y0():
    # GIVEN a multiline string with start and end
    map_string = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    world = Map.from_string(map_string)
    # WHEN trying to get the neighboring fields
    neighbor = world.get_neighbours(Field(x=0, y=0, elevation=0))
    # THEN the map should return the right neighbors (N, S, W, E)
    assert neighbor == (
        None,
        Field(x=0, y=1, elevation=0), #south
        None,
        Field(x=1, y=0, elevation=0), #east
        )

def test_get_neightbors_at_edge_x_max_y_max():
    # GIVEN a multiline string with start and end
    map_string = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    world = Map.from_string(map_string)
    # WHEN trying to get the neighboring fields
    neighbor = world.get_neighbours(Field(x=7, y=4, elevation=get_elevation_from_char('i', (7, 4))))
    # THEN the map should return the right neighbors (N, S, W, E)
    print(f"neighbor at edge max {neighbor}")
    assert neighbor == (
        Field(x=7, y=3, elevation=get_elevation_from_char('j', (7, 3))), #north
        None,
        Field(x=6, y=4, elevation=get_elevation_from_char('h', (6, 4))), #west
        None,
    )

def test_get_neightbors_field_out_of_range_x():
    # GIVEN a multiline string with start and end
    map_string = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    world = Map.from_string(map_string)
    # WHEN trying to get the neighboring fields of outside the map, x overrun
    neighbor = world.get_neighbours(Field(x=8, y=0, elevation=0))
    # THEN the map should return the right neighbors (N, S, W, E), which is None
    assert neighbor == None
    
def test_get_neightbors_field_out_of_range_y():
    # GIVEN a multiline string with start and end
    map_string = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    world = Map.from_string(map_string)
    # WHEN trying to get the neighboring fields of outside the map, y overrun
    neighbor = world.get_neighbours(Field(x=0, y=5, elevation=0))
    # THEN the map should return the right neighbors (N, S, W, E), which is None
    assert neighbor == None

def test_an_empty_map():
    # GIVEN an empty map
    map_string = """\
"""
    # WHEN creating an empty map
    world = Map.from_string(map_string)
    # THEN check the width and the height of the map
    assert world.height == 0
    assert world.width == 0