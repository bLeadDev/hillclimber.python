
import pytest
from src.model import Map, Field

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
    # THEN the map should contain a field with elevation 0 (=a) at (x=0, y=0)
    assert world.get_field(0, 0) == Field(x=0, y=0, elevation=0)
    # AND the map should contain a field with elevation 1 (=b) at (x=0, y=1)
    assert world.get_field(0, 1) == Field(x=0, y=1, elevation=1)
    assert world.get_field(0, 2) == Field(x=0, y=2, elevation=2)
    assert world.get_field(1, 0) == Field(x=1, y=0, elevation=0)
    assert world.get_field(1, 1) == Field(x=1, y=1, elevation=1)
    assert world.get_field(1, 2) == Field(x=1, y=2, elevation=0)
    assert world.get_field(2, 0) == Field(x=2, y=0, elevation=1)
    assert world.get_field(2, 1) == Field(x=2, y=1, elevation=0)
    assert world.get_field(2, 2) == Field(x=2, y=2, elevation=0)
    assert world.get_field(3, 0) == Field(x=3, y=0, elevation=2)
    assert world.get_field(3, 1) == Field(x=3, y=1, elevation=0)
    assert world.get_field(3, 2) == Field(x=3, y=2, elevation=2)