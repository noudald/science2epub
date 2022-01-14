# science2epub

Convert the current Science magazine to epub. This will only work when you
have a Science membership, as you have to login before the script scrapes
the Science website.

# Installation

You need to have pandoc installed. As this script uses selenium you have to
set your PATH to the correct geckodriver [https://selenium-python.readthedocs.io/installation.html#drivers].
To install all python requirements:
```
pip install -r requirements.txt
```

# How to run

```
python science2epub.py
```

Wait a couple of seconds to read the full index of the magazine. The login as
you usually would. After you logged in hit enter and wait till the epub is
created.
