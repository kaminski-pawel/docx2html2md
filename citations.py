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


def _find_all_citation_spans(html_soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    return html_soup.find_all("span", {"class": "citation"})


def _has_inner_json_data(span: bs4.Tag) -> bool:
    return span.attrs["data-src"].startswith("data:application/json;base64,")


def add_citations_and_bibliography(
    html_soup: bs4.BeautifulSoup, citation_style: str = "harvard1"
) -> bs4.BeautifulSoup:
    citations = extract_citations(html_soup)
    json_data = prepare_citations_for_citeproc(citations)
    bib_source = citeproc.source.json.CiteProcJSON(json_data)
    bib_style = citeproc.CitationStylesStyle(citation_style, validate=False)
    bibliography = citeproc.CitationStylesBibliography(
        bib_style, bib_source, citeproc.formatter.html
    )
    citeproc_citations = create_citations_to_register(citations)
    for citation in citeproc_citations:
        bibliography.register(citation)
    html_soup = add_citations(html_soup, citeproc_citations, citations, bibliography)
    return html_soup


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


def add_citations(
    html_soup: bs4.BeautifulSoup,
    citeproc_citations: list[citeproc.Citation],
    citations: list[Citation],
    bib: citeproc.CitationStylesBibliography,
) -> bs4.BeautifulSoup:
    i = 0
    spans = html_soup.find_all("span", {"class": "citation"})
    for span in spans:
        data_src = span.attrs["data-src"]
        # this should follow the same rule as in extract_citations()
        if data_src.startswith("data:application/json;base64,"):
            citation = citations[i]
            citation_str = citation["properties"]["plainCitation"]
            GENERATE_CITATION_USING_CITEPROC = (
                "citation = citeproc_citations[i]",
                "citation_str = bib.cite(citation, _warn)",
            )
            new_tag = html_soup.new_tag("cite")
            new_tag.string = citation_str
            span.replace_with(new_tag)
            i += 1
    return html_soup
