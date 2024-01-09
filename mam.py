import shutil
import subprocess
import mammoth
import pathlib

if __name__ == "__main__":
    fp = pathlib.Path("./04_docx_guidelines.docx")
    assert fp.exists()
    assert fp.is_dir() == False
    print(fp)
    with open(fp, "rb") as f:
        result = mammoth.convert_to_html(f)
        # result = mammoth.convert_to_markdown(f)
        print(result.value)
        print(result.messages)
    with open(fp.with_suffix(".html"), "w") as f:
        # with open(fp.with_suffix(".md"), "w") as f:
        f.write(result.value)

    shutil.copyfile("04_docx_guidelines.md", "jb/04_docx_guidelines.md")
    shutil.copyfile("04_docx_guidelines.md", "mystmd/04_docx_guidelines.md")
    subprocess.run("jupyter-book build jb/".split(" "))
