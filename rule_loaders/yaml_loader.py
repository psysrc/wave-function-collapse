import yaml
from pathlib import Path
from wfc.tile import TileDefinition
from wfc.basic_socket import SocketID, BasicSocket, SocketType


class YamlLoader:
    _supported_file_versions = [1]

    def __init__(self, yaml_file: Path) -> None:
        self._data = yaml.load(yaml_file.open(), Loader=yaml.Loader)

        match self._data:
            case {"version": version}:
                if version not in self._supported_file_versions:
                    raise RuntimeError(f"Unsupported file version {version}: (supported versions are {self._supported_file_versions})")

            case _:
                raise RuntimeError("Failed to get rule configuration version")

    def load(self) -> list[TileDefinition]:
        sockets = self._load_socket_data()

        raise NotImplementedError()

    def _load_socket_data(self) -> dict[SocketID, BasicSocket]:
        match self._data:
            case {"sockets": [*sockets]}:
                sockets = self._load_sockets(sockets)

                return {sock.get_id(): sock for sock in sockets}

            case _:
                raise RuntimeError("Failed to parse socket definitions")

    @staticmethod
    def _load_sockets(sockets_data: list) -> list[BasicSocket]:
        sockets: list[BasicSocket] = []

        for socket_data in sockets_data:
            match socket_data:
                case {"id": id, "type": "symmetric"}:
                    symmetric_socket = BasicSocket(id=id, type=SocketType.SYMMETRIC)
                    sockets.append(symmetric_socket)

                case {"id": id, "type": "asymmetric", "counterpart": counterpart}:
                    asymmetric_socket = BasicSocket(id=id, type=SocketType.ASYMMETRIC)
                    sockets.append(asymmetric_socket)
                    sockets.append(asymmetric_socket.asymmetric_counterpart())

                case _:
                    raise RuntimeError(f"Failed to parse socket definition: {repr(socket_data)}")

        return sockets
