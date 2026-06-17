# bsp_tool_docs

Documentation for [bsp_tool](https://github.com/snake-biscuits/bsp_tool)<br/>
Built with [Zensical](https://zensical.org/)<br/>
Inspired by [NorthstarDocs](https://github.com/R2Northstar/NorthstarDocs)


## Offline Testing

```sh
# on Debian-based Linux w/ venv & pip installed
$ python3 -m venv .env
$ source .env/bin/activate
(.env) $ python -m pip install --upgrade pip
(.env) $ python -m pip install zensical
(.env) $ zensical serve
# NOTE: zensical should hot-swap any edits while serving
# -- also, you might miss the link on the first line, but it is there
Serving .../site on http://localhost:8000
Build started
Warning: ...
... issue(s) found
# Ctrl+C to kill the server
^CReceived interrupt, exiting
(.env) $ exit
$
```

> `requirements.txt` is a relic from using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
