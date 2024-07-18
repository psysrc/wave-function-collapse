import yaml
from pathlib import Path
from wfc.tile import TileDefinition


class YamlLoader:
    _supported_file_versions = [1]

    def __init__(self, yaml_file: Path) -> None:
        self._data: dict = yaml.load(yaml_file.open(), Loader=yaml.Loader)

        if (file_version := self._data.get("version")) not in self._supported_file_versions:
            raise RuntimeError(f"Unsupported file version: {file_version} (supported versions are {self._supported_file_versions})")

    def load(self) -> list[TileDefinition]:
        raise NotImplementedError()
