import bs4
import citeproc
import mammoth
import pathlib
from pprint import pprint
import pytest

from citations import (
    create_citations_to_register,
    extract_citations,
    prepare_citations_for_citeproc,
    generate_citation,
)


# def test_extract_citations_from_fields():
#     html = """<p>A claim
#     <span class="citation"
#         data-src="data:application/json;base64,eyJjaXRhdGlvbklEIjoiUGRRWmdzekciLCJwcm9wZXJ0aWVzIjp7ImZvcm1hdHRlZENpdGF0aW9uIjoiKEhhbGwgMjAxMykiLCJwbGFpbkNpdGF0aW9uIjoiKEhhbGwgMjAxMykiLCJub3RlSW5kZXgiOjB9LCJjaXRhdGlvbkl0ZW1zIjpbeyJpZCI6NiwidXJpcyI6WyJodHRwOi8vem90ZXJvLm9yZy91c2Vycy9sb2NhbC9idjc0QXJFUS9pdGVtcy9UODVJTjJUWSJdLCJpdGVtRGF0YSI6eyJpZCI6NiwidHlwZSI6ImJvb2siLCJhYnN0cmFjdCI6IlJlc3BvbmRpbmcgdG8gdGhlIGdyb3d0aCBvZiBkaWdpdGFsIHByb2R1Y3RzIGFuZCB0aGUgY29tbWVyY2lhbCBpbXBlcmF0aXZlIHRvIGJ1aWxkIG5ldyBkaWdpdGFsIGJ1c2luZXNzZXMsIFRoZSBCdXNpbmVzcyBvZiBEaWdpdGFsIFB1Ymxpc2hpbmcgb2ZmZXJzIGEgY29tcHJlaGVuc2l2ZSBpbnRyb2R1Y3Rpb24gdG8gdGhlIGRldmVsb3BtZW50IG9mIGRpZ2l0YWwgcHJvZHVjdHMgaW4gdGhlIGJvb2sgYW5kIGpvdXJuYWwgaW5kdXN0cmllcy5cblxuVGhpcyB0ZXh0Ym9vayBwcm92aWRlcyBiYWNrZ3JvdW5kIHRvIHRoZSBtYWluIHRlY2hub2xvZ2ljYWwgZGV2ZWxvcG1lbnQgdGhhdCBoYXZlIGluZmx1ZW5jZWQgdGhlIGdyb3d0aCBvZiBkaWdpdGFsIHB1Ymxpc2hpbmcsIGludHJvZHVjaW5nIHN0dWRlbnRzIHRvIHRoZSBrZXkgdGVybXMgYW5kIGNvbmNlcHRzIHRoYXQgbWFrZSBkaWdpdGFsIHB1Ymxpc2hpbmcgcG9zc2libGUuXG5cbkV4cGxvcmluZyBmb3VyIGtleSBwdWJsaXNoaW5nIHNlY3RvcnM6IHByb2Zlc3Npb25hbCByZWZlcmVuY2UsIGFjYWRlbWljLCBlZHVjYXRpb24gYW5kIGNvbnN1bWVyLCB0aGlzIGJvb2sgZXhwbGFpbnMgdGhlIGNvbnRleHQgZm9yIHRoZSBkaWdpdGFsIGRldmVsb3BtZW50cyBpbiBlYWNoIGFyZWEgYW5kIGxvb2tzIGF0IHRoZSBncm93dGggb2YgbmV3IGJ1c2luZXNzIG1vZGVscyBhbmQgdGhlIGZ1dHVyZSBjaGFsbGVuZ2VzIGZhY2VkIGJ5IGVhY2ggc2VjdG9yLlxuXG5JdCBhbHNvIGFkZHJlc3NlcyB0aGUga2V5IGlzc3VlcyB0aGF0IGZhY2UgdGhlIGluZHVzdHJ5IGFzIGEgd2hvbGUsIG91dGxpbmluZyBjdXJyZW50IGRlYmF0ZXMsIHN1Y2ggYXMgcHJpY2luZyBhbmQgY29weXJpZ2h0LCBhbmQgZXhwbG9yaW5nIHRoZWlyIGltcGFjdCBvbiB0aGUgaW5kdXN0cnkgdGhyb3VnaCByZWxldmFudCBjYXNlIHN0dWRpZXMuXG5cblRoZSBCdXNpbmVzcyBvZiBEaWdpdGFsIFB1Ymxpc2hpbmcgaXMgYW4gaW52YWx1YWJsZSByZXNvdXJjZSBmb3IgYW55IHB1Ymxpc2hpbmcgc3R1ZGVudCBsb29raW5nIGZvciBhIHN0YXJ0aW5nIHBvaW50IGZyb20gd2hpY2ggdG8gZXhwbG9yZSB0aGUgd29ybGQgb2YgZGlnaXRhbCBwdWJsaXNoaW5nLiIsIklTQk4iOiI5NzgwNDE1NTA3MzE4IiwibnVtYmVyLW9mLXBhZ2VzIjoiMTk0IiwicHVibGlzaGVyIjoiUm91dGxlZGdlIiwidGl0bGUiOiJUaGUgQnVzaW5lc3Mgb2YgRGlnaXRhbCBQdWJsaXNoaW5nOiBBbiBJbnRyb2R1Y3Rpb24gdG8gdGhlIERpZ2l0YWwgQm9vayBhbmQgSm91cm5hbCBJbmR1c3RyaWVzIiwidGl0bGUtc2hvcnQiOiJUaGUgQnVzaW5lc3Mgb2YgRGlnaXRhbCBQdWJsaXNoaW5nIiwiYXV0aG9yIjpbeyJmYW1pbHkiOiJIYWxsIiwiZ2l2ZW4iOiJGcmFuaWEifV0sImlzc3VlZCI6eyJkYXRlLXBhcnRzIjpbWyIyMDEzIiw2LDE3XV19fX1dLCJzY2hlbWEiOiJodHRwczovL2dpdGh1Yi5jb20vY2l0YXRpb24tc3R5bGUtbGFuZ3VhZ2Uvc2NoZW1hL3Jhdy9tYXN0ZXIvY3NsLWNpdGF0aW9uLmpzb24ifSA="
#         hidden="hidden">
#     </span>
#     <a href="#citation_PdQZgszG">(Hall 2013)</a>.
#     </p>"""
#     html_soup = bs4.BeautifulSoup(html, "html.parser")
#     citations = extract_citations(html_soup)
#     assert len(citations) == 1
#     assert citations[0]["citationID"] == "PdQZgszG"
#     assert citations[0]["citationItems"][0]["itemData"]["type"] == "book"


# def test_extract_citations_from_footnotes():
#     html = """<p>A claim
#     <span class="citation"
#         data-src="data:application/json;base64,eyJjaXRhdGlvbklEIjoiUGRRWmdzekciLCJwcm9wZXJ0aWVzIjp7ImZvcm1hdHRlZENpdGF0aW9uIjoiKEhhbGwgMjAxMykiLCJwbGFpbkNpdGF0aW9uIjoiKEhhbGwgMjAxMykiLCJub3RlSW5kZXgiOjB9LCJjaXRhdGlvbkl0ZW1zIjpbeyJpZCI6NiwidXJpcyI6WyJodHRwOi8vem90ZXJvLm9yZy91c2Vycy9sb2NhbC9idjc0QXJFUS9pdGVtcy9UODVJTjJUWSJdLCJpdGVtRGF0YSI6eyJpZCI6NiwidHlwZSI6ImJvb2siLCJhYnN0cmFjdCI6IlJlc3BvbmRpbmcgdG8gdGhlIGdyb3d0aCBvZiBkaWdpdGFsIHByb2R1Y3RzIGFuZCB0aGUgY29tbWVyY2lhbCBpbXBlcmF0aXZlIHRvIGJ1aWxkIG5ldyBkaWdpdGFsIGJ1c2luZXNzZXMsIFRoZSBCdXNpbmVzcyBvZiBEaWdpdGFsIFB1Ymxpc2hpbmcgb2ZmZXJzIGEgY29tcHJlaGVuc2l2ZSBpbnRyb2R1Y3Rpb24gdG8gdGhlIGRldmVsb3BtZW50IG9mIGRpZ2l0YWwgcHJvZHVjdHMgaW4gdGhlIGJvb2sgYW5kIGpvdXJuYWwgaW5kdXN0cmllcy5cblxuVGhpcyB0ZXh0Ym9vayBwcm92aWRlcyBiYWNrZ3JvdW5kIHRvIHRoZSBtYWluIHRlY2hub2xvZ2ljYWwgZGV2ZWxvcG1lbnQgdGhhdCBoYXZlIGluZmx1ZW5jZWQgdGhlIGdyb3d0aCBvZiBkaWdpdGFsIHB1Ymxpc2hpbmcsIGludHJvZHVjaW5nIHN0dWRlbnRzIHRvIHRoZSBrZXkgdGVybXMgYW5kIGNvbmNlcHRzIHRoYXQgbWFrZSBkaWdpdGFsIHB1Ymxpc2hpbmcgcG9zc2libGUuXG5cbkV4cGxvcmluZyBmb3VyIGtleSBwdWJsaXNoaW5nIHNlY3RvcnM6IHByb2Zlc3Npb25hbCByZWZlcmVuY2UsIGFjYWRlbWljLCBlZHVjYXRpb24gYW5kIGNvbnN1bWVyLCB0aGlzIGJvb2sgZXhwbGFpbnMgdGhlIGNvbnRleHQgZm9yIHRoZSBkaWdpdGFsIGRldmVsb3BtZW50cyBpbiBlYWNoIGFyZWEgYW5kIGxvb2tzIGF0IHRoZSBncm93dGggb2YgbmV3IGJ1c2luZXNzIG1vZGVscyBhbmQgdGhlIGZ1dHVyZSBjaGFsbGVuZ2VzIGZhY2VkIGJ5IGVhY2ggc2VjdG9yLlxuXG5JdCBhbHNvIGFkZHJlc3NlcyB0aGUga2V5IGlzc3VlcyB0aGF0IGZhY2UgdGhlIGluZHVzdHJ5IGFzIGEgd2hvbGUsIG91dGxpbmluZyBjdXJyZW50IGRlYmF0ZXMsIHN1Y2ggYXMgcHJpY2luZyBhbmQgY29weXJpZ2h0LCBhbmQgZXhwbG9yaW5nIHRoZWlyIGltcGFjdCBvbiB0aGUgaW5kdXN0cnkgdGhyb3VnaCByZWxldmFudCBjYXNlIHN0dWRpZXMuXG5cblRoZSBCdXNpbmVzcyBvZiBEaWdpdGFsIFB1Ymxpc2hpbmcgaXMgYW4gaW52YWx1YWJsZSByZXNvdXJjZSBmb3IgYW55IHB1Ymxpc2hpbmcgc3R1ZGVudCBsb29raW5nIGZvciBhIHN0YXJ0aW5nIHBvaW50IGZyb20gd2hpY2ggdG8gZXhwbG9yZSB0aGUgd29ybGQgb2YgZGlnaXRhbCBwdWJsaXNoaW5nLiIsIklTQk4iOiI5NzgwNDE1NTA3MzE4IiwibnVtYmVyLW9mLXBhZ2VzIjoiMTk0IiwicHVibGlzaGVyIjoiUm91dGxlZGdlIiwidGl0bGUiOiJUaGUgQnVzaW5lc3Mgb2YgRGlnaXRhbCBQdWJsaXNoaW5nOiBBbiBJbnRyb2R1Y3Rpb24gdG8gdGhlIERpZ2l0YWwgQm9vayBhbmQgSm91cm5hbCBJbmR1c3RyaWVzIiwidGl0bGUtc2hvcnQiOiJUaGUgQnVzaW5lc3Mgb2YgRGlnaXRhbCBQdWJsaXNoaW5nIiwiYXV0aG9yIjpbeyJmYW1pbHkiOiJIYWxsIiwiZ2l2ZW4iOiJGcmFuaWEifV0sImlzc3VlZCI6eyJkYXRlLXBhcnRzIjpbWyIyMDEzIiw2LDE3XV19fX1dLCJzY2hlbWEiOiJodHRwczovL2dpdGh1Yi5jb20vY2l0YXRpb24tc3R5bGUtbGFuZ3VhZ2Uvc2NoZW1hL3Jhdy9tYXN0ZXIvY3NsLWNpdGF0aW9uLmpzb24ifSA="
#         hidden="hidden">
#     </span>
#     <a href="#citation_PdQZgszG">(Hall 2013)</a>.</p>"""
#     html_soup = bs4.BeautifulSoup(html, "html.parser")
#     citations = extract_citations(html_soup)
#     assert len(citations) == 1
#     assert citations[0]["citationID"] == "PdQZgszG"
#     assert citations[0]["citationItems"][0]["itemData"]["type"] == "book"


class TestCitationsFromFields:
    fp = pathlib.Path("citation_in_footnotes.docx")

    @classmethod
    def setup_class(cls):
        with open(cls.fp, "rb") as f:
            result = mammoth.convert_to_html(
                f, style_map="p[style-name='Quote'] => cite:fresh"
            )
        cls.html_soup = bs4.BeautifulSoup(result.value, "html.parser")

    def test_extract_citations(self):
        citations = extract_citations(self.html_soup)
        assert len(citations) == 2

        citations[0]["citationItems"][0]["itemData"]["type"] == "article-journal"
        citations[0]["citationItems"][0]["itemData"]["title"] = "Just no"
        citations[0]["citationItems"][0]["itemData"]["author"][0]["family"] == "Schmoe"

        citations[1]["citationItems"][0]["itemData"]["type"] == "chapter"
        citations[1]["citationItems"][0]["itemData"]["title"] = "I disagree"
        citations[1]["citationItems"][0]["itemData"]["author"][0]["family"] == "Ce"

        citations[1]["citationItems"][1]["itemData"]["type"] == "book"
        citations[1]["citationItems"][1]["itemData"]["title"] = "Zażółć gęślą jaźń"
        citations[1]["citationItems"][1]["itemData"]["author"][0]["family"] == "Ce"
        citations[1]["citationItems"][1]["itemData"]["event-place"] == "안돌이지돌이다래미한숨바우"

    def test_prepare_citations_for_citeproc(self):
        citations = extract_citations(self.html_soup)
        json_data = prepare_citations_for_citeproc(citations)
        bib_source = citeproc.source.json.CiteProcJSON(json_data)
        bib_style = citeproc.CitationStylesStyle("harvard1", validate=False)
        bib = citeproc.CitationStylesBibliography(
            bib_style, bib_source, citeproc.formatter.html
        )
        citeproc_citations = create_citations_to_register(citations)
        for citation in citeproc_citations:
            bib.register(citation)
        citation_generator = generate_citation(self.html_soup, citeproc_citations, bib)
        citation_1 = next(citation_generator)
        citation_2 = next(citation_generator)
        assert citation_1 == "(Schmoe 2035)"
        assert citation_2 == "(Ce 2010; Ce 2023)"
        with pytest.raises(StopIteration):
            next(citation_generator)
