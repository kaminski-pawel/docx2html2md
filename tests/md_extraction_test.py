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
        cls.assmeta0 = cls.metadata.assets[0]
        cls.assmeta1 = cls.metadata.assets[1]
        cls.assmeta2 = cls.metadata.assets[2]
        cls.expected_meta = [
            {
                "papersrc": pathlib.Path("./images/tiny-picture.png"),
                "licensename": "Unsplash License",
                "licenseurl": "https://unsplash.com/license",
                "author": "Jean Carlo Emer",
                "takenfrom": "https://unsplash.com/photos/beige-concrete-house-2d-RL-xa4mk",
            },
            {
                "papersrc": pathlib.Path("./images/10x10px-img.png"),
                "digitalsrc": pathlib.Path("./images/10x10px-img.png"),
                "deleteprev": False,
                "author": "Koziołek Matołek",
            },
            {
                "papersrc": pathlib.Path("./images/10x10px-img.png"),
                "deleteprev": True,
            },
        ]

    def test_all_metadata_tables_were_extracted(self):
        assert len(self.metadata.assets) == 3

    def test_all_metadata_rows_were_extracted(self):
        assert len(self.metadata.assets[0]) == len(self.expected_meta[0])
        assert len(self.metadata.assets[1]) == len(self.expected_meta[1])

    def test_string_values(self):
        assert self.assmeta0["papersrc"] == self.expected_meta[0]["papersrc"]
        assert self.assmeta0["licensename"] == self.expected_meta[0]["licensename"]
        assert self.assmeta0["licenseurl"] == self.expected_meta[0]["licenseurl"]
        assert self.assmeta0["author"] == self.expected_meta[0]["author"]
        assert self.assmeta1["author"] == self.expected_meta[1]["author"]

    def test_filepath_values(self):
        assert self.assmeta0["papersrc"] == self.expected_meta[0]["papersrc"]
        assert self.assmeta1["papersrc"] == self.expected_meta[1]["papersrc"]
        assert self.assmeta1["digitalsrc"] == self.expected_meta[1]["digitalsrc"]

    def test_filepath_attribs(self):
        assert self.assmeta0.paper_fp == pathlib.Path("./images/tiny-picture.png")
        assert self.assmeta0.digital_fp == None
        assert self.assmeta1.paper_fp == pathlib.Path("./images/10x10px-img.png")
        assert self.assmeta1.digital_fp == pathlib.Path("./images/10x10px-img.png")
        assert self.assmeta2.paper_fp == pathlib.Path("./images/tiny-picture.png")
        assert self.assmeta2.digital_fp == pathlib.Path("./images/10x10px-img.png")

    def test_delete_prev_values(self):
        assert "deleteprev" not in self.assmeta0.__dict__
        assert self.assmeta1["deleteprev"] == self.expected_meta[1]["deleteprev"]
        assert self.assmeta2["deleteprev"] == self.expected_meta[2]["deleteprev"]

    def test_delete_prev_attrib(self):
        assert self.assmeta0.delete_prev == False
        assert self.assmeta1.delete_prev == False
        assert self.assmeta2.delete_prev

    def test_metadata_tables_removed_from_markdown(self):
        assert self.assmeta0["licensename"] not in self.md
        assert self.assmeta0["author"] not in self.md
        assert self.assmeta1["author"] not in self.md

    def test_standard_tables_included_in_markdown(self):
        assert (
            "\n|  |  |\n| --- | --- |\n| Just a table | Just a table |\n| Don’t extract | Don’t extract |\n\n"
            in self.md
        )
