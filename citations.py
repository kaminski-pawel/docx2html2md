import base64
import bs4
import json
import typing as t


class CitationItem(t.TypedDict):
    id: t.Union[int, str]
    itemData: dict[str, t.Any]  # TODO: extend itemData with explicit TypedDict
    uris: list[str]


class CitationItemProps(t.TypedDict):
    formattedCitation: str
    noteIndex: int
    plainCitation: str


class Citation(t.TypedDict):
    citationID: str
    citationItems: list[CitationItem]
    properties: CitationItemProps
    schema: str


def extract_citations(html_soup: bs4.BeautifulSoup) -> list[Citation]:
    citations = []
    spans = html_soup.find_all("span", {"class": "citation"})
    for span in spans:
        data_src = span.attrs["data-src"]
        if data_src.startswith("data:application/json;base64,"):
            citations.append(
                json.loads(
                    base64.b64decode(data_src[len("data:application/json;base64,") :]),
                    strict=False,
                )
            )
    return citations
