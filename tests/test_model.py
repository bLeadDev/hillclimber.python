
import pytest
from src.model import Map, Field, Walker, get_elevation_from_char

def test_create_a_walker_who_is_able_to_climb_one_up():
    walker = Walker(Field(x=0, y=0, elevation=0))
    assert(walker.can_climb(Field(x=1, y=0, elevation=1)) == True)

def test_create_a_walker_who_is_able_to_climb_down():
    walker = Walker(Field(x=0, y=0, elevation=15))
    assert(walker.can_climb(Field(x=1, y=0, elevation=1)) == True)

def test_create_a_walker_who_is_not_able_to_climb_up_more_than_one():
    walker = Walker(Field(x=0, y=0, elevation=0))
    assert(walker.can_climb(Field(x=1, y=0, elevation=2)) == False)

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
    neighbor = world.get_neighbours(Field(x=7, y=4, elevation=get_elevation_from_char('i')))
    # THEN the map should return the right neighbors (N, S, W, E)
    print(f"neighbor at edge max {neighbor}")
    assert neighbor == (
        Field(x=7, y=3, elevation=get_elevation_from_char('j')), #north
        None,
        Field(x=6, y=4, elevation=get_elevation_from_char('h')), #west
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

