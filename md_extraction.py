import dataclasses
import json
import pathlib
import typing as t
import uuid


# Only the first item is the final key,
# the others are valid but will be mapped to the first item
METADATA_MAPPING_PAPER_SRC = ["papersrc", "papersource", "src", "source"]
METADATA_MAPPING_DIGITAL_SRC = ["digitalsrc", "digitalsource"]
METADATA_MAPPING_DEL_PREV = [
    "deleteprev",
    "deleteprevious",
    "removeprev",
    "removeprevious",
]
METADATA_MAPPING_TAKEN_FROM = ["from", "takenfrom"]
# Type cast values based on the keys
KEY_FOR_BOOLEANS = [*METADATA_MAPPING_DEL_PREV]
# To normalize table keys create a mapping {"oldkey": "normalizedkey"}
METADATA_MAPPING = {}
for mapping in [
    METADATA_MAPPING_PAPER_SRC,
    METADATA_MAPPING_DIGITAL_SRC,
    # METADATA_MAPPING_GENERAL_SRC,
    METADATA_MAPPING_DEL_PREV,
    METADATA_MAPPING_TAKEN_FROM,
]:
    METADATA_MAPPING.update({old: mapping[0] for old in mapping[1:]})


# type AcceptedValues = t.Union[str, bool, pathlib.Path] # TODO: upgrade to Python 3.12


@dataclasses.dataclass
class AssetDatapoint:
    _key: str
    _val: str
    key: str = dataclasses.field(init=False)
    val: t.Union[str, bool, pathlib.Path] = dataclasses.field(init=False)

    def __post_init__(self):
        self.key = self._normalize_key()
        if self.key in KEY_FOR_BOOLEANS:
            self.val = self._val_to_bool()
        elif self._looks_like_a_potential_filepath():
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
        s = self._key
        while " " in s:
            s = s.replace(" ", "")
        s = s.lower().strip().replace("_", "").replace("-", "").replace("#", "")
        if s in METADATA_MAPPING:
            return METADATA_MAPPING[s]
        return s

    def _val_to_bool(self) -> bool:
        v = self._val.strip().lower()
        if v in [
            "0",
            "no",
            "nee",
            "not",
            "non",
            "nul",
            "none",
            "nicht",
            "nein",
            "false",
            "kein",
        ]:
            return False
        return bool(v)

    def to_dict(self):
        return {self.key: self.val}

    def to_json(self):
        return {self.key: str(self.val)}


class AssetMetadata:
    """
    Container of key:val pairs describing a single asset
    (e.g. license and author data of a single image)
    """

    def __init__(self) -> None:
        self.uuid = str(uuid.uuid4())
        self._datapoints = []
        self.paper_fp = None
        self.digital_fp = None
        self.delete_prev = False

    def __getitem__(self, key: str) -> t.Union[str, bool, pathlib.Path]:
        return self.__dict__[key]

    def __nonzero__(self):
        return bool(self._datapoints)

    def to_dict(self) -> dict[str, t.Union[str, bool, pathlib.Path]]:
        return {dp.key: dp.val for dp in self._datapoints}

    def add(self, key: str, val: str) -> None:
        datapoint = AssetDatapoint(_key=key, _val=val)
        if datapoint.key in METADATA_MAPPING_DEL_PREV:
            self.delete_prev = datapoint.val
        elif isinstance(datapoint.val, pathlib.Path):
            if datapoint.key in METADATA_MAPPING_PAPER_SRC:
                self.paper_fp = datapoint.val
            elif datapoint.key in METADATA_MAPPING_DIGITAL_SRC:
                self.digital_fp = datapoint.val
        self._datapoints.append(datapoint)
        self.__dict__[datapoint.key] = datapoint.val

    def remove(self, key: str) -> None:
        for dp, i in enumerate(self._datapoints):
            if dp.key == key:
                del self._datapoints[i]

    def includes(self, key: str) -> bool:
        for dp in self._datapoints:
            if dp.key == key:
                return True
        return False

    def __str__(self):
        return json.dumps([dp.to_json() for dp in self._datapoints])

    def __len__(self):
        return len(self._datapoints)


class BookMetadata:
    def __init__(self) -> None:
        self.assets = []
        self._metadata = {}

    def __getitem__(self, key: str) -> AssetMetadata:
        return self._metadata[key]

    def add_asset_metadata(self, asset_meta: AssetMetadata) -> None:
        self._metadata[asset_meta.uuid] = asset_meta
        self.assets.append(asset_meta)

    def assets_as_dicts(self) -> list[dict[str, t.Union[str, bool, pathlib.Path]]]:
        return [am.to_dict() for am in self.assets]

    def __str__(self) -> str:
        return "%s(assets=[%s])" % (
            self.__class__.__name__,
            ", ".join(str(am) for am in self.assets),
        )
