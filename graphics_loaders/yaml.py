from pathlib import Path
from typing import Any
import yaml
from wfc.tile import TileID


class YamlGraphicsLoader:
    _supported_file_versions = [1]

    def __init__(self, yaml_file: Path) -> None:
        self._data = yaml.load(yaml_file.open(), Loader=yaml.Loader)

        match self._data:
            case {"version": version}:
                if version not in self._supported_file_versions:
                    raise RuntimeError(f"Unsupported file version {version}: (supported versions are {self._supported_file_versions})")

            case _:
                raise RuntimeError("Failed to get graphics configuration version")

    def load(self) -> dict[TileID, Path]:
        match self._data:
            case {"tiles": [*tiles]}:
                return self._load_tiles(tiles)

            case _:
                raise RuntimeError("Failed to parse graphics entries")

    @staticmethod
    def _load_tiles(tiles: list[Any]) -> dict[TileID, Path]:
        graphics: dict[TileID, Path] = {}

        for tile in tiles:
            match tile:
                case {"id": id, "graphic": str(path)}:
                    if not isinstance(id, TileID):
                        raise RuntimeError(f"Entry ID '{id}' is not the expected type {TileID}")

                    graphics[id] = Path(path)

                case _:
                    raise RuntimeError(f"Failed to parse entry: {repr(tile)}")

        return graphics
