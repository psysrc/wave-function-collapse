from abc import ABC, abstractmethod


class Socket(ABC):
    """An abstract socket type supported by the WFC implementation."""

    @abstractmethod
    def compatible_with(self, other: "Socket") -> bool:
        """Calculate whether this and another socket are compatible or not."""


SocketSet = set[Socket]
