import bs4
import mammoth
import pathlib

from citations import add_citations_and_bibliography
from html2md import convert_to_md
from md_extraction import BookMetadata


class TestHtml2MdFootnotes:
    fp = pathlib.Path("citation_in_footnotes.docx")

    @classmethod
    def setup_class(cls):
        with open(cls.fp, "rb") as f:
            result = mammoth.convert_to_html(f)
        cls.html_soup = bs4.BeautifulSoup(result.value, "html.parser")
        cls.html_soup = add_citations_and_bibliography(cls.html_soup)
        metadata = BookMetadata()
        cls.md = convert_to_md(cls.html_soup, metadata)

    def test_footnote_ref_properly_converted_to_myst_syntax(self):
        expected_md_start = "Claim A[^footnote-ref-1]. Claim B[^footnote-ref-2]."
        assert self.md.startswith(expected_md_start)

    def test_footnotes_properly_converted_to_myst_syntax(self):
        expected_md_includes = (
            "[^footnote-ref-1]: Joe Schmoe, „Just no“, Opinions, 1, Nr. 1 (2035): 1–2."
        )
        assert expected_md_includes in self.md
