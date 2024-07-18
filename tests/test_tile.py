from wfc.tile import *
from wfc.abstract_socket import Socket

class TestSocket(Socket):
    __test__ = False  # Stops pytest trying to collect this class

    def __init__(self, id: int) -> None:
        self._id = id

    def compatible_with(self, other: Socket) -> bool:
        if isinstance(other, TestSocket):
            return self._id == other._id

        return False


def test_rotate_socket_sets_none():
    a = TestSocket(1)
    b = TestSocket(2)
    c = TestSocket(3)
    d = TestSocket(4)

    socket_sets: DirectionalSocketSetMap = {
        Direction.UP: {a},
        Direction.RIGHT: {b},
        Direction.DOWN: {c},
        Direction.LEFT: {d},
    }

    expected_socket_sets: DirectionalSocketSetMap = {
        Direction.UP: {a},
        Direction.RIGHT: {b},
        Direction.DOWN: {c},
        Direction.LEFT: {d},
    }

    assert rotate_socket_sets(socket_sets, Rotation.NONE) == expected_socket_sets


def test_rotate_socket_sets_clockwise():
    a = TestSocket(1)
    b = TestSocket(2)
    c = TestSocket(3)
    d = TestSocket(4)

    socket_sets: DirectionalSocketSetMap = {
        Direction.UP: {a},
        Direction.RIGHT: {b},
        Direction.DOWN: {c},
        Direction.LEFT: {d},
    }

    expected_socket_sets: DirectionalSocketSetMap = {
        Direction.UP: {d},
        Direction.RIGHT: {a},
        Direction.DOWN: {b},
        Direction.LEFT: {c},
    }

    assert rotate_socket_sets(socket_sets, Rotation.CLOCKWISE) == expected_socket_sets


def test_rotate_socket_sets_half():
    a = TestSocket(1)
    b = TestSocket(2)
    c = TestSocket(3)
    d = TestSocket(4)

    socket_sets: DirectionalSocketSetMap = {
        Direction.UP: {a},
        Direction.RIGHT: {b},
        Direction.DOWN: {c},
        Direction.LEFT: {d},
    }

    expected_socket_sets: DirectionalSocketSetMap = {
        Direction.UP: {c},
        Direction.RIGHT: {d},
        Direction.DOWN: {a},
        Direction.LEFT: {b},
    }

    assert rotate_socket_sets(socket_sets, Rotation.HALF) == expected_socket_sets


def test_rotate_socket_sets_anticlockwise():
    a = TestSocket(1)
    b = TestSocket(2)
    c = TestSocket(3)
    d = TestSocket(4)

    socket_sets: DirectionalSocketSetMap = {
        Direction.UP: {a},
        Direction.RIGHT: {b},
        Direction.DOWN: {c},
        Direction.LEFT: {d},
    }

    expected_socket_sets: DirectionalSocketSetMap = {
        Direction.UP: {b},
        Direction.RIGHT: {c},
        Direction.DOWN: {d},
        Direction.LEFT: {a},
    }

    assert rotate_socket_sets(socket_sets, Rotation.ANTICLOCKWISE) == expected_socket_sets
