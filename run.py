import datetime
import hashlib
import shutil
import subprocess
import time
import bs4
import os

# from bs4 import BeautifulSoup
import mammoth
import pathlib

# from markdownify import markdownify as md
from html2md import convert_to_md
from citations import add_citations_and_bibliography
from md_extraction import BookMetadata
from metadata_extraction import replace_assets_with_directives

DATA_DIR = "data/"

# https://jupyterbook.org/en/stable/reference/cheatsheet.html#executable-code
# ENABLE_EXECUTABLE_CODE_IN_JB = """---
# jupytext:
#   text_representation:
#     extension: .md
#     format_name: myst
# kernelspec:
#   display_name: Python 3
#   language: python
#   name: python3
# ---

# """


def _copy_to_data_dir(fp: pathlib.Path) -> pathlib.Path:
    newfp = pathlib.Path(DATA_DIR, fp.name)
    shutil.copyfile(fp, newfp)
    return newfp


# cls.metadata = BookMetadata()
# cls.html_soup = add_citations_and_bibliography(cls.html_soup)
# cls.html_soup = assets_metadata(cls.html_soup, cls.metadata)
# cls.md = convert_to_md(cls.html_soup, cls.metadata)


def _prepare_md(fp: pathlib.Path) -> None:
    # transform .docx to .html
    style_mappings = """
    p[style-name='Quote'] => blockquote:fresh
    """
    # p[style-name='Quote'] => cite:fresh
    with open(fp, "rb") as f:
        result = mammoth.convert_to_html(f, style_map=style_mappings)
        # print(result.value)
        # print(result.messages)

    # extract metadata from tables in result.value (copyrights, etc.)

    # extract bibliography as json in citation style language
    html_soup = bs4.BeautifulSoup(result.value, "html.parser")
    metadata = BookMetadata()
    html_soup = add_citations_and_bibliography(html_soup)
    html_soup = replace_assets_with_directives(html_soup, metadata)

    with open(fp.with_suffix(".html"), "w") as f:
        f.write(str(html_soup))

    # transform .html to .md file
    with open(fp.with_suffix(".md"), "w") as f:
        # markdown = ENABLE_EXECUTABLE_CODE_IN_JB + convert_to_md(result.value)
        f.write(convert_to_md(html_soup, metadata))


def _render_digital_version(fp: pathlib.Path) -> None:
    # prepare a jupyter-notebook and mystmd rendering of the .md file
    shutil.copyfile(fp.with_suffix(".md"), f"jb/{fp.with_suffix('.md').name}")
    shutil.copyfile(fp.with_suffix(".md"), f"mystmd/{fp.with_suffix('.md').name}")
    subprocess.run(
        "jupyter-book build jb/".split(" ")
    )  # when tested around 1.5 sec perf_time() 😬
    WORKS_GREAT_BUT_IS_SLOWER_THAN_JB = (
        'subprocess.Popen("myst build --html".split(" "), cwd="mystmd/")'
        # hard to measure: builds fast, but then has to spin up a server
    )


BOOK_PATH = "/mnt/c/Users/Pawel.kaminski/OneDrive - University of Luxembourg/Digital Monography Documents/Guidelines for Drafting Manuscripts"
LATENCY_TEST = "/mnt/c/Users/Pawel.kaminski/OneDrive - University of Luxembourg/Digital Monography Documents/2024-02-05_review-january/latency-test.docx"


if __name__ == "__main__":
    last_modified = {}
    while True:
        for fp in [
            # pathlib.Path("./citation_in_fields.docx"),
            # pathlib.Path("./citation_in_footnotes.docx"),
            # pathlib.Path("./cross-references.docx"),
            # pathlib.Path("./quick-loop.docx"),
            # pathlib.Path("./local-latency-test.docx"),
            # pathlib.Path(LATENCY_TEST),
            pathlib.Path("./embedded_widgets.docx"),
        ]:
            # pass
            # for fp in pathlib.Path(BOOK_PATH).glob("*.docx"):
            if not fp.exists() or fp.is_dir():
                continue
            if fp.name.startswith("~$"):
                continue
            if fp not in last_modified:
                last_modified[fp] = 0
                # last_modified[fp] = fp.stat().st_mtime
            # print(
            #     "mtime=",
            #     datetime.datetime.fromtimestamp(fp.stat().st_mtime),
            #     "; cached=",
            #     datetime.datetime.fromtimestamp(last_modified[fp]),
            # )
            if fp.stat().st_mtime > last_modified[fp]:
                "Update recognized"
                localfp = _copy_to_data_dir(fp)
                _prepare_md(localfp)
                _render_digital_version(localfp)
                last_modified[fp] = fp.stat().st_mtime
            time.sleep(2)
            print("...")
