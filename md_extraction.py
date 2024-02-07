import dataclasses  # import dataclass
import json
import pathlib
import typing as t


METADATA_MAPPING_FILE_LOCATION = {"#Location": "#Location"}
METADATA_MAPPING = {**METADATA_MAPPING_FILE_LOCATION}


@dataclasses.dataclass
class AssetDatapoint:
    _key: str
    _val: str
    key: str = dataclasses.field(init=False)
    val: t.Union[str, pathlib.Path] = dataclasses.field(init=False)

    def __post_init__(self):
        self.key = self._key.strip()
        if self._looks_like_a_potential_filepath():
            fp = pathlib.Path(self._val)
            self.val = fp
        # TODO: consider adding an url handler
        else:
            self.val = self._val.strip()

    def _looks_like_a_potential_filepath(self):
        # TODO: after clarity on the asset storage, change this naive
        # logic into `if fp.exists() and not fp.is_dir()` or similar
        if self._val.startswith("./"):
            return True
        return False

    def to_dict(self):
        return {self.key: self.val}

    def to_json(self):
        return {self.key: str(self.val)}


class AssetMetadata:
    """
    Container of key:val pairs re. 1 asset
    (e.g. license and author data of a single image)
    """

    def __init__(self) -> None:
        self.datapoints = []
        self.file = None

    def to_dict(self) -> list[AssetDatapoint]:
        return {dp.key: dp.val for dp in self.datapoints}

    def add(self, key: str, val: str) -> None:
        datapoint = AssetDatapoint(_key=key, _val=val)
        if (
            isinstance(datapoint.val, pathlib.Path)
            and key in METADATA_MAPPING_FILE_LOCATION
        ):
            self.file = datapoint.val
        self.datapoints.append(datapoint)

    def remove(self, key: str) -> None:
        for dp, i in enumerate(self.datapoints):
            if dp.key == key:
                del self.datapoints[i]

    def includes(self, key: str) -> bool:
        for dp in self.datapoints:
            if dp.key == key:
                return True
        return False

    def __str__(self):
        return json.dumps([dp.to_json() for dp in self.datapoints])

    def __len__(self):
        return len(self.datapoints)


class BookMetadata:
    def __init__(self) -> None:
        self.assets = []

    def sayhi(self):
        print("\n\nHi!\n\n")
        return "Hi"

    def add_asset_metadata(self, asset_meta: AssetMetadata) -> None:
        self.assets.append(asset_meta)

    def assets_as_dicts(self) -> dict[str, t.Union[str, pathlib.Path]]:
        return [am.to_dict() for am in self.assets]

    def __str__(self):
        return "%s(assets=[%s])" % (
            self.__class__.__name__,
            ", ".join(str(am) for am in self.assets),
        )
