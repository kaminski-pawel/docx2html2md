import dataclasses  # import dataclass
import json
import pathlib
import typing as t


METADATA_MAPPING_PAPER_SRC = ["papersrc", "papersource"]
METADATA_MAPPING_DIGITAL_SRC = ["digitalsrc", "digitalsource"]
METADATA_MAPPING_GENERAL_SRC = ["src", "source"]
METADATA_MAPPING_DEL_PREV = [
    "deleteprev",
    "deleteprevious",
    "removeprev",
    "removeprevious",
]
METADATA_MAPPING_TAKEN_FROM = ["from", "takenfrom"]
METADATA_MAPPINGS = [
    METADATA_MAPPING_PAPER_SRC,
    METADATA_MAPPING_DIGITAL_SRC,
    METADATA_MAPPING_GENERAL_SRC,
    METADATA_MAPPING_DEL_PREV,
    METADATA_MAPPING_TAKEN_FROM,
]
METADATA_MAPPING = {}
# To normalize table keys create a mapping {"oldkey": "normalizedkey"}
for mapping in METADATA_MAPPINGS:
    METADATA_MAPPING.update({old: mapping[0] for old in mapping[1:]})


print("METADATA_MAPPING", METADATA_MAPPING)


@dataclasses.dataclass
class AssetDatapoint:
    _key: str
    _val: str
    key: str = dataclasses.field(init=False)
    val: t.Union[str, pathlib.Path] = dataclasses.field(init=False)

    def __post_init__(self):
        self.key = self._normalize_key()
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

    def _normalize_key(self) -> str:
        s = (
            self._key.lower()
            .strip()
            .replace("_", "")
            .replace("-", "")
            .replace("#", "")
            .replace(" ", "")
        )
        if s in METADATA_MAPPING:
            return METADATA_MAPPING[s]
        return s

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
        self.paper_fp = None
        self.digital_fp = None

    def __getitem__(self, key: str) -> t.Union[str, pathlib.Path]:
        return self.__dict__[key]

    def to_dict(self) -> list[AssetDatapoint]:
        return {dp.key: dp.val for dp in self.datapoints}

    def add(self, key: str, val: str) -> None:
        datapoint = AssetDatapoint(_key=key, _val=val)
        if isinstance(datapoint.val, pathlib.Path):
            if datapoint.key in METADATA_MAPPING_PAPER_SRC:
                self.paper_fp = datapoint.val
                if self.digital_fp is None:
                    self.digital_fp = datapoint.val
            elif datapoint.key in METADATA_MAPPING_DIGITAL_SRC:
                self.digital_fp = datapoint.val
                if self.paper_fp is None:
                    self.paper_fp = datapoint.val
            elif datapoint.key in METADATA_MAPPING_GENERAL_SRC:
                self.paper_fp = datapoint.val
                self.digital_fp = datapoint.val
        self.datapoints.append(datapoint)
        self.__dict__[datapoint.key] = datapoint.val

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
