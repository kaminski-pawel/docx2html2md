import shutil
import subprocess
import bs4

# from bs4 import BeautifulSoup
import mammoth
import pathlib

# from markdownify import markdownify as md
from html2md import convert_to_md
from citations import add_citations_and_bibliography

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


def _run_on(fp: pathlib.Path) -> None:
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
    html_soup = add_citations_and_bibliography(html_soup)

    with open(fp.with_suffix(".html"), "w") as f:
        f.write(str(html_soup))

    # transform .html to .md file
    with open(fp.with_suffix(".md"), "w") as f:
        # markdown = ENABLE_EXECUTABLE_CODE_IN_JB + convert_to_md(result.value)
        f.write(convert_to_md(html_soup))

    # prepare a jupyter-notebook and mystmd rendering of the .md file
    shutil.copyfile(fp.with_suffix(".md"), f"jb/{fp.with_suffix('.md').name}")
    shutil.copyfile(fp.with_suffix(".md"), f"mystmd/{fp.with_suffix('.md').name}")
    subprocess.run("jupyter-book build jb/".split(" "))  # around 1.5 sec perf_time() 😬
    WORKS_GREAT_BUT_IS_SLOWER_THAN_JB = (
        'subprocess.Popen("myst build --html".split(" "), cwd="mystmd/")'
        # hard to measure: builds fast, but then has to spin up a server
    )


if __name__ == "__main__":
    for fp in [
        # pathlib.Path("./citation_in_fields.docx"),
        # pathlib.Path("./citation_in_footnotes.docx"),
        pathlib.Path("./04_docx_guidelines.docx"),
    ]:
        assert fp.exists()
        assert fp.is_dir() == False
        print(fp)
        _run_on(fp)
