
import pytest
import sys
from src.model import Map, Field, Walker, Path, ShortestPathFinder, get_elevation_from_char

#############################
#
# SOLVING TESTS
# 
#############################
#@pytest.mark.skip(reason="Work in progress")
def test_solving_a_single_line_map():
    # GIVEN a single line string
    map_string = """\
ab"""

    # WHEN creating a map from the string creating the walker with the world and the path with the walker
    world = Map.from_string(map_string)
    world.set_start(0, 0)
    world.set_end(1, 0)
    walker = Walker(world)
    path = Path(walker)
    
    # THEN the right path should be found 
    shortest = ShortestPathFinder.solve(world, path, walker)
    assert shortest.fields == [Field(0, 0, 0), Field(1, 0, 1)]

#@pytest.mark.skip(reason="Work in progress")
def test_solving_a_small_multi_line_map():

    # GIVEN a mutli line string, an empty path and a walker at pos 0, 0
    map_string = """\
ad
bc"""
    # WHEN creating a map from the string creating the walker with the world and the path with the walker
    world = Map.from_string(map_string)
    world.set_start(0, 0)
    world.set_end(1, 1)
    walker = Walker(world)
    path = Path(walker)
    
    # THEN the path length should be 3 and contain these fields
    shortest_path = ShortestPathFinder().solve(world, path, walker)
    assert shortest_path.get_length() == 3
    print(f"{shortest_path.fields}")
    assert shortest_path.fields == [Field(0, 0, 0), Field(0, 1, 1), Field(1, 1, 2)]

#pytest.mark.skip(reason="Work in progress")
def test_solving_a_middle_multi_line_map_start_in_middle_go_down():

    # GIVEN a mutli line string, an empty path and a walker at pos 1, 1
    map_string = """\
fbf
bab
fbf"""
    # WHEN creating a map from the string creating the walker with the world and the path with the walker
    world = Map.from_string(map_string)
    world.set_start(1, 1)
    world.set_end(1, 2)
    walker = Walker(world)
    path = Path(walker)

    # THEN the path should contain these 2 fields, start and down
    shortest_path = ShortestPathFinder().solve(world, path, walker)

    assert shortest_path.fields == [Field(1, 1, 0), Field(1, 2, 1)]
                                                          
#@pytest.mark.skip(reason="Work in progress")
def test_solving_a_middle_multi_line_map_start_in_middle_go_left():

    # GIVEN a mutli line string, an empty path and a walker at pos 1, 1
    map_string = """\
fbf
bab
fbf"""
    world = Map.from_string(map_string)
    world.set_start(1, 1)
    world.set_end(0, 1)
    walker = Walker(world)
    path = Path(walker)

    # THEN the path should contain these 2 fields, start and left
    shortest_path = ShortestPathFinder().solve(world, path, walker)

    assert shortest_path.fields == [Field(1, 1, 0), Field(0, 1, 1)]

@pytest.mark.skip(reason="Not yet sure how")
def test_solving_a_middle_multi_line_map_start_in_middle_unreachable():

    # GIVEN a mutli line string, an empty path and a walker at pos
    map_string = """\
fbf
bab
fbf"""
    world = Map.from_string(map_string)
    world.set_start(1, 1)
    world.set_end(0, 0)
    walker = Walker(world)
    path = Path(walker)


    # THEN the path length should be 5 
    with pytest.raises(Exception) as excinfo:
        shortest_path = ShortestPathFinder().solve(world, path, walker)
    assert str(excinfo.value) == "Unsolvable map!"

#@pytest.mark.skip(reason="Work in progress")
def test_solving_a_middle_multi_line_map_start_at_edge_round_corner():

    # GIVEN a mutli line string, an empty path and a walker at pos 0, 1
    map_string = """\
fbf
bab
fbf"""
    world = Map.from_string(map_string)
    world.set_start(0, 1)
    world.set_end(1, 0)
    walker = Walker(world)
    path = Path(walker)

    # THEN the path length should be 5 
    shortest_path = ShortestPathFinder().solve(world, path, walker)

    assert shortest_path.fields == [Field(0, 1, 1), Field(1, 1, 0), Field(1, 0, 1)]

#@pytest.mark.skip(reason="Work in progress")
def test_solving_a_multi_line_map_with_obstacle_and_downclimb():

    # GIVEN a mutli line string with obstacle and downclimb, an empty path and a walker at pos 0, 0
    map_string = """\
abda
abcd"""
    world = Map.from_string(map_string)
    world.set_start(0, 0)
    world.set_end(3, 0)
    walker = Walker(world)
    path = Path(walker)
    
    # THEN the path length should be 5 and the field should be 3, 0
    shortest = ShortestPathFinder.solve(world, path, walker)

    assert shortest.get_length() == 5
    assert shortest.get_end() == Field(3, 0, 0)

#@pytest.mark.skip(reason="Work in progress")
def test_solving_a_multi_line_map_with_obstacle_and_downclimb():

    # GIVEN a mutli line string with obstacle, an empty path and a walker at pos 0, 0
    map_string = """\
abda
abcd"""
    world = Map.from_string(map_string)
    world.set_start(0, 0)
    world.set_end(3, 0)
    walker = Walker(world)
    path = Path(walker)
    
    # THEN the path length should be 6 and field should be 3, 0
    shortest = ShortestPathFinder.solve(world, path, walker)

    assert shortest.get_length() == 6
    assert shortest.get_end() == Field(3, 0, 0)

#@pytest.mark.skip(reason="Work in progress")
def test_solving_a_multi_line_map_with_obstacle():

    # GIVEN a mutli line string with obstacle, an empty path and a walker at pos 0, 0
    map_string = """\
abdc
abcd"""
    world = Map.from_string(map_string)
    world.set_start(0, 0)
    world.set_end(3, 0)
    walker = Walker(world)
    path = Path(walker)
    
    # THEN the path length should be 6 and ending 3, 0, 2
    shortest = ShortestPathFinder.solve(world, path, walker)

    assert shortest.get_length() == 6
    assert shortest.get_end() == Field(3, 0, 2)

#@pytest.mark.skip(reason="Work in progress")
def test_solving_small_full_test_map_():

    # GIVEN a mutli line string with a full map 
    map_string = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

    world = Map.from_string(map_string)
    walker = Walker(world)
    path = Path(walker)

    # THEN the path length should be 31 and the ending field 2, 5, 25
    shortest = ShortestPathFinder.solve(world, path, walker)

    assert shortest.get_length() == 32 # Length of path is 32 because the starting field is also included in path
    assert shortest.get_end() == Field(5, 2, 25)


@pytest.mark.skip(reason="Data too big")
def test_solving_full_test_map_():

    # GIVEN a mutli line string with a full map 
    map_string = """\
abacccaaaacccccccccccaaaaaacccccaaaaaaccccaaacccccccccccccccccccccccccccccccccccccccccccaaaaa
abaaccaaaacccccccccccaaaaaaccccccaaaaaaaaaaaaaccccccccccccccccccccccccccccccccccccccccccaaaaa
abaaccaaaacccccccccccaaaaacccccaaaaaaaaaaaaaaaccccccccccccccccccccccccccccccccccccccccccaaaaa
abccccccccccccccccccccaaaaacccaaaaaaaaaaaaaaaacccccccccccccccccccccccccccaaaccccccccccccaaaaa
abccccccccccccccccccccaacaacccaaaaaaaaccaaaaaccccccccccccccccccccccccccccaaaccccccccccccaccaa
abcccccccccccccaacccaaaccccccaaaaaaaaaccaaaaaccccccccccccccccccccccccccccccacccccccccccccccca
abcccccccccccaaaaaaccaaaccacccccaaaaaaacccccccccccccccccccccccccciiiicccccccddddddccccccccccc
abcccccccccccaaaaaaccaaaaaaaccccaaaaaacccccaacccccccaaaccccccccciiiiiiiicccdddddddddacaaccccc
abccccccccccccaaaaaaaaaaaaacccccaaaaaaacaaaacccccccaaaacccccccchhiiiiiiiiicddddddddddaaaccccc
abcccccccccccaaaaaaaaaaaaaacccccccaaacccaaaaaacccccaaaaccccccchhhipppppiiiijjjjjjjddddaaccccc
abcccccccccccaaaaaaaaaaaaaaccccccccccccccaaaaaccccccaaaccccccchhhpppppppiijjjjjjjjjddeeaccccc
abcccccccccccccccccaaaaaaaacccccccccccccaaaaaccccccccccccccccchhppppppppppjjqqqjjjjjeeeaacccc
abccccccccccccccccccaaaaaaaacccccccccccccccaacccccccccccccccchhhpppuuuupppqqqqqqqjjjeeeaacccc
abcccccccccccccccccccaacccacccccccccccccccccccccccccccccccccchhhopuuuuuuppqqqqqqqjjjeeecccccc
abacccccccccccccaaacaaaccccccccccccccccccccccccccccaaccccccchhhhoouuuuuuuqvvvvvqqqjkeeecccccc
abaccccccccccccaaaaaacccccaaccccccccccccccccccccccaaaccccccchhhooouuuxxxuvvvvvvqqqkkeeecccccc
abaccccccccccccaaaaaacccaaaaaaccccccccccccccccccaaaaaaaaccchhhhooouuxxxxuvyyyvvqqqkkeeecccccc
abcccccccccccccaaaaacccaaaaaaaccccccccccccccccccaaaaaaaaccjjhooooouuxxxxyyyyyvvqqqkkeeecccccc
abccccccccccccccaaaaaacaaaaaaaccccccccaaaccccccccaaaaaaccjjjooootuuuxxxxyyyyyvvqqkkkeeecccccc
abccccccccccccccaaaaaaaaaaaaacccccccccaaaacccccccaaaaaacjjjooootttuxxxxxyyyyvvrrrkkkeeecccccc
SbccccccccccccccccccaaaaaaaaacccccccccaaaacccccccaaaaaacjjjoootttxxxEzzzzyyvvvrrrkkkfffcccccc
abcccccccccccaaacccccaaaaaaacaaaccccccaaaccccccccaaccaacjjjoootttxxxxxyyyyyyvvvrrkkkfffcccccc
abcccccccccaaaaaacccaaaaaacccaaacacccaacccccccccccccccccjjjoootttxxxxyxyyyyyywvvrrkkkfffccccc
abcccccccccaaaaaacccaaaaaaaaaaaaaaaccaaacaaacccccaacccccjjjnnnttttxxxxyyyyyyywwwrrkkkfffccccc
abcaacacccccaaaaacccaaacaaaaaaaaaaaccaaaaaaacccccaacaaacjjjnnnntttttxxyywwwwwwwwrrrlkfffccccc
abcaaaaccccaaaaacccccccccaacaaaaaaccccaaaaaacccccaaaaacccjjjnnnnnttttwwywwwwwwwrrrrllfffccccc
abaaaaaccccaaaaaccccccaaaaaccaaaaacaaaaaaaaccccaaaaaaccccjjjjinnnntttwwwwwsssrrrrrllllffccccc
abaaaaaaccccccccccccccaaaaacaaaaaacaaaaaaaaacccaaaaaaacccciiiiinnnntswwwwssssrrrrrlllfffccccc
abacaaaaccccccccccccccaaaaaacaaccccaaaaaaaaaaccccaaaaaaccccciiiinnnssswwsssssllllllllfffccccc
abccaaccccccccccccccccaaaaaaccccccccccaaacaaaccccaaccaacccccciiiinnsssssssmmllllllllfffaacccc
abccccccccccccccccccccaaaaaaccccccccccaaaccccccccaaccccccccccciiinnmsssssmmmmlllllgggffaacccc
abcccccccccccccccaccccccaaacccccccccccaaccccccccccccccccccccccciiimmmsssmmmmmgggggggggaaacccc
abcccccccccaaaaaaaaccccccccccccccccccccccccccccaaaaaccccccccccciiimmmmmmmmmgggggggggaaacccccc
abccccccccccaaaaaaccccccccccccccccccaacccccccccaaaaacccccccccccciiimmmmmmmhhggggcaaaaaaaccccc
abccccccccccaaaaaacccccccccccccccccaacccccccccaaaaaacccccccccccciihhmmmmhhhhgccccccccaacccccc
abccccaacaaaaaaaaaaccccccccccccccccaaaccccccccaaaaaaccccccccccccchhhhhhhhhhhaaccccccccccccccc
abccccaaaaaaaaaaaaaaccccccccccaaccaaaaccccccccaaaaaacccaaacccccccchhhhhhhhaaaaccccccccccccccc
abcccaaaaaaaaaaaaaaaccccccccaaaaaacaaaacacaccccaaaccccaaaacccccccccchhhhccccaaccccccccccaaaca
abcccaaaaaacacaaacccccccccccaaaaaaaaaaaaaaacccccccccccaaaacccccccccccaaaccccccccccccccccaaaaa
abcccccaaaacccaaaccccccccccaaaaaaaaaaaaaaaaccccccccccccaaacccccccccccaaacccccccccccccccccaaaa
abcccccaacccccaacccccccccccaaaaaaaaaaaaaccccccccccccccccccccccccccccccccccccccccccccccccaaaaa"""

    world = Map.from_string(map_string)
    walker = Walker(world)
    path = Path(walker)

    # THEN the path length should be 31 and the ending field 2, 5, 25
    shortest = ShortestPathFinder.solve(world, path, walker)

    assert shortest.get_length() == 32 # Length of path is 32 because the starting field is also included in path
    assert shortest.get_end() == Field(5, 2, 25)


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

def test_count_climable_neighbors_with_two():
    # GIVEN a multi line string with start and end 
    map_string = """\
ab
ba"""

    # WHEN creating a map from the string, and then creating the walker with the map, and setting start and end
    world = Map.from_string(map_string)
    world.set_start(0, 0)
    walker = Walker(world)

    # THEN the walker should be able to climb 2
    assert walker.count_climbable_neighbors(world.get_neighbours(walker.position)) == 2

def test_count_climable_neighbors_with_3_middle():
    # GIVEN a multi line string with start and end 
    map_string = """\
aaa
ada
aza"""

    # WHEN creating a map from the string, and then creating the walker with the map, and setting start and end
    world = Map.from_string(map_string)
    world.set_start(1, 1)
    walker = Walker(world)

    # THEN the walker should be able to climb 2
    assert walker.count_climbable_neighbors(world.get_neighbours(walker.position)) == 3


def test_create_a_walker_set_start_end_checking_start():
    # GIVEN a multi line string with start and end 
    map_string = """\
ab
ca"""

    # WHEN creating a map from the string, and then creating the walker with the map, and setting start and end
    world = Map.from_string(map_string)
    world.set_start(1, 1)
    world.set_end(0, 0)
    walker = Walker(world)

    # THEN the walker should start at the right position
    assert walker.position == Field(1, 1, 0)

def test_create_a_walker_from_map_with_end_and_start_checking_position():
    # GIVEN a multi line string with start and end 
    map_string = """\
abbd
sfSb
dasf
asfE"""

    # WHEN creating a map from the string, and then creating the walker with the map
    world = Map.from_string(map_string)
    walker = Walker(world)

    # THEN the walker should start at the right position
    assert walker.position == Field(2, 1, 0)

def test_create_a_walker_set_start_end_checking_path():
    # GIVEN a multi line string with start and end 
    map_string = """\
adfalndglc
agasdaxff
fdsddfasf
agssadfvb"""

    # WHEN creating a map from the string and setting start and end,
    # creating the walker with the wolrd and the path with the walker
    world = Map.from_string(map_string)
    world.set_start(1, 1)
    world.set_end(3, 3)
    walker = Walker(world)
    path = Path(walker)

    # THEN the path should start at the right position
    assert path.fields[0] == (Field(1, 1, get_elevation_from_char('g', (1, 1)))) 


#############################
#
# MAP AND FIELD TESTS
# 
#############################

def test_add_a_field_to_a_map():
    # GIVEN an empty map
    world = Map()
    world.width = 1
    world.height = 1
    # WHEN adding a new field (x=0, y=0, elevation 5)
    world.add_field(0, 0, 5)

    # THEN the map should contain a field with elevation 5 at (x=0, y=0)
    assert world.get_field(0, 0) == Field(0, 0, 5)

def test_adding_multiple_fields_to_a_map():
    # GIVEN an empty map
    world = Map()
    world.width = 2
    world.height = 2
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
        # THEN the map should throw an error that indicates too many starting points
    with pytest.raises(Exception) as excinfo:
        world = Map.from_string(map_string)
    assert str(excinfo.value) == "Multiple starting points detected!"


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
        Field(x=0, y=-1, elevation=sys.maxsize), #north
        Field(x=0, y=1, elevation=0), #south
        Field(x=-1, y=0, elevation=sys.maxsize), #west
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
        Field(x=7, y=5, elevation=sys.maxsize), #south
        Field(x=6, y=4, elevation=get_elevation_from_char('h', (6, 4))), #west
        Field(x=8, y=4, elevation=sys.maxsize), #east
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
    assert neighbor == (
        Field(x=8, y=-1, elevation=sys.maxsize), #north
        Field(x=8, y=1, elevation=sys.maxsize), #south
        Field(x=7, y=0, elevation=get_elevation_from_char('m', (7,0))), #west
        Field(x=9, y=0, elevation=sys.maxsize), #east
        )
    
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
    assert neighbor == (
        Field(x=0, y=4, elevation=get_elevation_from_char('a', (0, 4))), #north
        Field(x=0, y=6, elevation=sys.maxsize), #south
        Field(x=-1, y=5, elevation=sys.maxsize), #west
        Field(x=1, y=5, elevation=sys.maxsize), #east
        )

def test_an_empty_map():
    # GIVEN an empty map
    map_string = """\
"""
    # WHEN creating an empty map
    world = Map.from_string(map_string)
    # THEN check the width and the height of the map
    assert world.height == 0
    assert world.width == 0

def test_add_2_steps():
    # GIVEN a Path with 2 steps
    p = Path()
    #WHEN I add two steps
    p.add_step(Field(0, 0, 77))
    p.add_step(Field(0, 1, 77))
    #THEN I expect a length of two and the coords (0,0), (0,1)
    assert p.fields[0] == (Field(0, 0, 77))
    assert p.fields[1] == (Field(0, 1, 77)) 
    assert p.get_length() == 2
            

def test_visited_fields_visited():
    # GIVEN A Path with  steps
    p = Path()
    p.add_step(Field(0, 0, 77))
    p.add_step(Field(1, 0, 77))
    p.add_step(Field(1, 1, 77))
    # WHEN i asked if there was a step on a visited field
    already_visited = p.field_visited(Field(1, 0,77))
    # THEN the test should be true
    assert already_visited == True

def test_visited_fields_unvisited():
    # GIVEN A Path with some steps
    p = Path()
    p.add_step(Field(0, 0, 77))
    p.add_step(Field(1, 0, 77))
    p.add_step(Field(1, 1, 77))
    # WHEN i asked if i steped on a field already
    already_visited = p.field_visited(Field(0, 3, 77))
    # THEN the test should be false, because there was no step on a visited field
    assert already_visited == False
    
def test_remove_last_step():
    # GIVEN an empty Path 
    p = Path()
    # WHEN adding three steps (length = 3)
    p.add_step(Field(0, 0, 10))
    p.add_step(Field(1, 0, 10))
    p.add_step(Field(2, 0, 10))    
    # THEN the last step should be deleted
    expected_fields = [(Field(0, 0, 10)), (Field(1, 0, 10))]
    p.remove_last_step()
    assert p.fields == expected_fields