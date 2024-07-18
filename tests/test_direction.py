from helpers.direction import *


def test_opposites():
    assert opposite_direction[Direction.UP] == Direction.DOWN
    assert opposite_direction[Direction.DOWN] == Direction.UP
    assert opposite_direction[Direction.LEFT] == Direction.RIGHT
    assert opposite_direction[Direction.RIGHT] == Direction.LEFT


def test_clockwise_movement():
    assert move_clockwise[Direction.UP] == Direction.RIGHT
    assert move_clockwise[Direction.RIGHT] == Direction.DOWN
    assert move_clockwise[Direction.DOWN] == Direction.LEFT
    assert move_clockwise[Direction.LEFT] == Direction.UP


def test_anticlockwise_movement():
    assert move_anticlockwise[Direction.UP] == Direction.LEFT
    assert move_anticlockwise[Direction.LEFT] == Direction.DOWN
    assert move_anticlockwise[Direction.DOWN] == Direction.RIGHT
    assert move_anticlockwise[Direction.RIGHT] == Direction.UP
