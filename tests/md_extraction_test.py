import bs4
import mammoth
import pathlib

from citations import add_citations_and_bibliography
from html2md import convert_to_md
from md_extraction import BookMetadata


class TestHtml2MdMetadataExtraction:
    fp = pathlib.Path("metadata_extraction.docx")

    @classmethod
    def setup_class(cls):
        with open(cls.fp, "rb") as f:
            result = mammoth.convert_to_html(f)
        cls.html_soup = bs4.BeautifulSoup(result.value, "html.parser")
        cls.html_soup = add_citations_and_bibliography(cls.html_soup)
        cls.metadata = BookMetadata()
        cls.md = convert_to_md(cls.html_soup, cls.metadata)
        cls.assets_meta = cls.metadata.assets_as_dicts()
        cls.expected_meta = [
            {
                "##Location": pathlib.Path("./images/tiny-picture.png"),
                "##License-name": "Unsplash License",
                "##License-url": "https://unsplash.com/license",
                "##Author": "Jean Carlo Emer",
                "##Source": "https://unsplash.com/photos/beige-concrete-house-2d-RL-xa4mk",
            },
            {
                "##Location": pathlib.Path("./images/10x10px-img.png"),
                "##Author": "Koziołek Matołek",
            },
        ]

    def test_all_metadata_tables_were_extracted(self):
        assert len(self.metadata.assets) == 2

    def test_all_metadata_rows_were_extracted(self):
        assert len(self.metadata.assets[0]) == 5
        assert len(self.metadata.assets[1]) == 2

    def test_string_values(self):
        assert (
            self.assets_meta[0]["##License-name"]
            == self.expected_meta[0]["##License-name"]
        )
        assert (
            self.assets_meta[0]["##License-url"]
            == self.expected_meta[0]["##License-url"]
        )
        assert self.assets_meta[0]["##Author"] == self.expected_meta[0]["##Author"]
        assert self.assets_meta[0]["##Source"] == self.expected_meta[0]["##Source"]
        assert self.assets_meta[1]["##Author"] == self.expected_meta[1]["##Author"]

    def test_filepath_values(self):
        assert self.assets_meta[0]["##Location"] == self.expected_meta[0]["##Location"]
        assert self.assets_meta[1]["##Location"] == self.expected_meta[1]["##Location"]

    def test_metadata_tables_removed_from_markdown(self):
        assert self.assets_meta[0]["##Author"] not in self.md
        assert self.assets_meta[1]["##Author"] not in self.md
        assert self.assets_meta[0]["##License-name"] not in self.md

    def test_standard_tables_included_in_markdown(self):
        assert (
            "\n|  |  |\n| --- | --- |\n| Just a table | Just a table |\n| Don’t extract | Don’t extract |\n\n"
            in self.md
        )
