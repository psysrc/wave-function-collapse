from helpers.rotation import *


def test_clockwise_rotation():
    assert rotate_clockwise[Rotation.NONE] == Rotation.CLOCKWISE
    assert rotate_clockwise[Rotation.CLOCKWISE] == Rotation.HALF
    assert rotate_clockwise[Rotation.HALF] == Rotation.ANTICLOCKWISE
    assert rotate_clockwise[Rotation.ANTICLOCKWISE] == Rotation.NONE


def test_anticlockwise_rotation():
    assert rotate_anticlockwise[Rotation.NONE] == Rotation.ANTICLOCKWISE
    assert rotate_anticlockwise[Rotation.ANTICLOCKWISE] == Rotation.HALF
    assert rotate_anticlockwise[Rotation.HALF] == Rotation.CLOCKWISE
    assert rotate_anticlockwise[Rotation.CLOCKWISE] == Rotation.NONE
