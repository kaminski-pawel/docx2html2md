import base64
import bs4
import json
import typing as t
import citeproc


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
            # we append data that has this shape:
            # {
            #     'citationID': 'a22p6p0ob48',
            #     'properties': {'formattedCitation': '\\uldash{see Abe Ce, \\uc0\\u8222{}I disagree\\uc0\\u8220{}, in {\\i{}We all agree} (Like Minded Publ, 2010), 12; Abe Ce, {\\i{}Za\\uc0\\u380{}\\uc0\\u243{}\\uc0\\u322{}\\uc0\\u263{} g\\uc0\\u281{}\\uc0\\u347{}l\\uc0\\u261{} ja\\uc0\\u378{}\\uc0\\u324{}}, UTF-16 Enjoyers (\\uc0\\u50504{}\\uc0\\u46028{}\\uc0\\u51060{}\\uc0\\u51648{}\\uc0\\u46028{}\\uc0\\u51060{}\\uc0\\u45796{}\\uc0\\u47000{}\\uc0\\u48120{}\\uc0\\u54620{}\\uc0\\u49704{}\\uc0\\u48148{}\\uc0\\u50864{}, 2023).}', 'plainCitation': 'see Abe Ce, „I disagree“, in We all agree (Like Minded Publ, 2010), 12; Abe Ce, Zażółć gęślą jaźń, UTF-16 Enjoyers (안돌이지돌이다래미한숨바우, 2023).',
            #                    'noteIndex': 2},
            #     'citationItems': [
            #         {
            #             'id': 43,
            #             'uris': ['http://zotero.org/users/local/bv74ArEQ/items/8ANM4ZRU'],
            #             'itemData': {
            #                 'id': 43,
            #                 'type': 'chapter',
            #                 'container-title': 'We all agree',
            #                 'publisher': 'Like Minded Publ',
            #                 'title': 'I disagree',
            #                 'author': [{'family': 'Ce', 'given': 'Abe'}],
            #                 'issued': {'date-parts': [['2010', 12, 31]]}
            #             },
            #             'locator': '12',
            #             'label': 'page',
            #             'prefix': 'see'
            #         },
            #         {
            #             'id': 41,
            #             'uris': ['http://zotero.org/users/local/bv74ArEQ/items/D2ZHM7Z4'],
            #             'itemData': {
            #                 'id': 41,
            #                 'type': 'book',
            #                 'collection-title': 'UTF-16 Enjoyers',
            #                 'event-place': '안돌이지돌이다래미한숨바우',
            #                 'publisher-place': '안돌이지돌이다래미한숨바우',
            #                 'title': 'Zażółć gęślą jaźń',
            #                 'author': [{'family': 'Ce', 'given': 'Abe'}],
            #                 'issued': {'date-parts': [['2023', 1, 1]]}
            #             }
            #         }
            #     ],
            #     'schema': 'https://github.com/citation-style-language/schema/raw/master/csl-citation.json'
            # }
    return citations


# t.Any could use the same type hint as `itemData`
def prepare_citations_for_citeproc(citations: list[Citation]) -> dict[str, t.Any]:
    citeproc_input = []
    for citation_group in citations:
        for citation_item in citation_group["citationItems"]:
            citeproc_input.append(citation_item["itemData"])
    return citeproc_input


def create_citations_to_register(citations: list[Citation]) -> list[citeproc.Citation]:
    """
    Processing citations in a document needs to be done in two passes as for some
    CSL styles, a citation can depend on the order of citations in the
    bibliography and thus on citations following the current one.
    For this reason, we first need to register all citations with the
    CitationStylesBibliography.
    """
    citation_objects = []
    for citation_group in citations:
        citation_items = []
        for citation_item in citation_group["citationItems"]:
            cit_id = str(citation_item["itemData"]["id"])
            citation_items.append(citeproc.CitationItem(cit_id))
        citation_objects.append(citeproc.Citation(citation_items))
    return citation_objects


def _warn(citation_item):
    print(
        "WARNING: Reference with key '{}' not found in the bibliography.".format(
            citation_item.key
        )
    )


def generate_citation(
    html_soup: bs4.BeautifulSoup,
    citations: list[citeproc.Citation],
    bib: citeproc.CitationStylesBibliography,
) -> t.Generator[str, None, None]:
    # ) -> list[str]:
    i = 0
    spans = html_soup.find_all("span", {"class": "citation"})
    for span in spans:
        data_src = span.attrs["data-src"]
        if data_src.startswith("data:application/json;base64,"):
            citation = citations[i]
            yield bib.cite(citation, _warn)
            # x.append(bib.cite(citation, _warn))
            i += 1  # this should follow the same rule as in extract_citations()
