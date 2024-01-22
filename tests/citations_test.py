import bs4
import citeproc
import mammoth
import pathlib

from citations import (
    add_citations,
    create_citations_to_register,
    extract_citations,
    prepare_citations_for_citeproc,
)


class TestCitationsFromFields:
    fp = pathlib.Path("citation_in_fields.docx")

    @classmethod
    def setup_class(cls):
        with open(cls.fp, "rb") as f:
            result = mammoth.convert_to_html(f)
        cls.html_soup = bs4.BeautifulSoup(result.value, "html.parser")
        cls.citations = extract_citations(cls.html_soup)
        json_data = prepare_citations_for_citeproc(cls.citations)
        bib_source = citeproc.source.json.CiteProcJSON(json_data)
        bib_style = citeproc.CitationStylesStyle("harvard1", validate=False)
        cls.bibliography = citeproc.CitationStylesBibliography(
            bib_style, bib_source, citeproc.formatter.html
        )
        cls.citeproc_citations = create_citations_to_register(cls.citations)
        for citation in cls.citeproc_citations:
            cls.bibliography.register(citation)
        cls.html_soup = add_citations(
            cls.html_soup, cls.citeproc_citations, cls.citations, cls.bibliography
        )

    def test_extract_citations_finds_all_citations(self):
        assert len(self.citations) == 1

    def test_extract_citations_properly_decodes_json_data(self):
        assert self.citations[0]["citationItems"][0]["label"] == "figure"
        assert self.citations[0]["citationItems"][0]["locator"] == "13"
        assert self.citations[0]["citationItems"][0]["prefix"] == "see"
        assert self.citations[0]["citationItems"][0]["suffix"] == "for examples"
        assert (
            self.citations[0]["citationItems"][0]["itemData"]["title"] == "I disagree"
        )
        assert (
            self.citations[0]["properties"]["plainCitation"]
            == "(see Ce 2010, Abb. 13 for examples)"
        )

    def test_render_proper_html(self):
        expected_html = (
            "<p>A claim <cite>(see Ce 2010, Abb. 13 for examples)</cite>.</p>"
        )
        assert str(self.html_soup) == expected_html


class TestCitationsFromFootnotes:
    fp = pathlib.Path("citation_in_footnotes.docx")

    @classmethod
    def setup_class(cls):
        with open(cls.fp, "rb") as f:
            result = mammoth.convert_to_html(f)
        cls.html_soup = bs4.BeautifulSoup(result.value, "html.parser")
        cls.citations = extract_citations(cls.html_soup)
        json_data = prepare_citations_for_citeproc(cls.citations)
        bib_source = citeproc.source.json.CiteProcJSON(json_data)
        bib_style = citeproc.CitationStylesStyle("harvard1", validate=False)
        cls.bibliography = citeproc.CitationStylesBibliography(
            bib_style, bib_source, citeproc.formatter.html
        )
        cls.citeproc_citations = create_citations_to_register(cls.citations)
        for citation in cls.citeproc_citations:
            cls.bibliography.register(citation)
        cls.html_soup = add_citations(
            cls.html_soup, cls.citeproc_citations, cls.citations, cls.bibliography
        )

    def test_extract_citations_finds_all_2_citations(self):
        assert len(self.citations) == 2

    def test_extract_citations_properly_decodes_json_data(self):
        assert (
            self.citations[0]["citationItems"][0]["itemData"]["type"]
            == "article-journal"
        )
        assert self.citations[0]["citationItems"][0]["itemData"]["title"] == "Just no"
        assert (
            self.citations[0]["citationItems"][0]["itemData"]["author"][0]["family"]
            == "Schmoe"
        )

        assert self.citations[1]["citationItems"][0]["itemData"]["type"] == "chapter"
        assert (
            self.citations[1]["citationItems"][0]["itemData"]["title"] == "I disagree"
        )
        assert (
            self.citations[1]["citationItems"][0]["itemData"]["author"][0]["family"]
            == "Ce"
        )

        assert self.citations[1]["citationItems"][1]["itemData"]["type"] == "book"
        assert (
            self.citations[1]["citationItems"][1]["itemData"]["title"]
            == "Zażółć gęślą jaźń"
        )
        assert (
            self.citations[1]["citationItems"][1]["itemData"]["author"][0]["family"]
            == "Ce"
        )
        assert (
            self.citations[1]["citationItems"][1]["itemData"]["event-place"]
            == "안돌이지돌이다래미한숨바우"
        )
        assert (
            self.citations[0]["properties"]["plainCitation"]
            == "Joe Schmoe, „Just no“, Opinions, 1, Nr. 1 (2035): 1–2."
        )

    def test_render_proper_html(self):
        expected_html_start = (
            "<p>Claim A<sup>"
            '<a href="#footnote-1" id="footnote-ref-1">[1]</a>'
            "</sup>. Claim B<sup>"
            '<a href="#footnote-2" id="footnote-ref-2">[2]</a>'
            "</sup>.</p>"
            '<ol><li id="footnote-1"><p> '
            "<cite>Joe Schmoe, „Just no“, Opinions, 1, Nr. 1 (2035): 1–2.</cite> "
            '<a href="#footnote-ref-1">↑</a>'
        )
        assert str(self.html_soup).startswith(expected_html_start)
