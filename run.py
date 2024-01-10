import shutil
import subprocess
import mammoth
import pathlib

# from markdownify import markdownify as md
from html2md import convert_to_md

if __name__ == "__main__":
    fp = pathlib.Path("./04_docx_guidelines.docx")
    assert fp.exists()
    assert fp.is_dir() == False
    print(fp)

    # transform .docx to .html
    style_mappings = """
    p[style-name='Quote'] => cite:fresh
    """
    with open(fp, "rb") as f:
        result = mammoth.convert_to_html(f, style_map=style_mappings)
        print(result.value)
        print(result.messages)
    with open(fp.with_suffix(".html"), "w") as f:
        f.write(result.value)

    # transform .html to .md file
    with open(fp.with_suffix(".md"), "w") as f:
        f.write(convert_to_md(result.value))

    # prepare a jupyter-notebook and mystmd rendering of the .md file
    shutil.copyfile(fp.with_suffix(".md"), f"jb/{fp.with_suffix('.md').name}")
    shutil.copyfile(fp.with_suffix(".md"), f"mystmd/{fp.with_suffix('.md').name}")
    subprocess.run("jupyter-book build jb/".split(" "))
    WORKS_GREAT_BUT_IS_SLOWER_THAN_JB = (
        'subprocess.Popen("myst build --html".split(" "), cwd="mystmd/")'
    )
