# Usage

To transform docx to md

```sh
python pre.py
python pandoc.py
python post.py
```

To start myst local web server

```sh
cd mystmd
myst start
```

If you are using WSL on Windows, you can run index.html in your favorite browser after opening it with a command:

```sh
cd jb/_build/html; explorer.exe .;cd ../../..
```
