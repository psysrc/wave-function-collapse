from enum import Enum
from wfc.abstract_socket import Socket


SocketID = int | str


class SocketType(Enum):
    SYMMETRIC = 0
    ASYMMETRIC = 1


class BasicSocket(Socket):
    def __init__(self, id: SocketID, type: SocketType) -> None:
        self._id = id
        self._type = type
        self._flipped = False

    def get_id(self) -> SocketID:
        return self._id

    def compatible_with(self, other: Socket) -> bool:
        """Decide if this socket is compatible with another socket or not."""

        if not isinstance(other, BasicSocket):
            return False

        if self._id != other._id:
            return False

        if self._type != other._type:
            raise RuntimeError(f"Socket ID {self._id} has inconsistent socket types")

        if self._type == SocketType.SYMMETRIC:
            return True

        if self._type == SocketType.ASYMMETRIC:
            return self._flipped != other._flipped

        raise RuntimeError(f"Couldn't deduce socket compatibility: '{repr(self)}' / '{repr(other)}'")

    def asymmetric_counterpart(self) -> "BasicSocket":
        if self._type != SocketType.ASYMMETRIC:
            raise RuntimeError(f"Cannot create asymmetric counterpart of non-asymmetric socket ID {self._id}")

        counterpart = BasicSocket(self._id, self._type)
        counterpart._flipped = not self._flipped

        return counterpart
