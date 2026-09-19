# bsp_tool_docs

Documentation for [bsp_tool](https://github.com/snake-biscuits/bsp_tool)<br/>
Built with [ProperDocs](https://properdocs.org/)<br/>
Inspired by [NorthstarDocs](https://github.com/R2Northstar/NorthstarDocs)


## Offline Testing

```sh
# on Gentoo Linux w/ venv & pip installed
$ python -m venv .env  # first time only
$ source .env/bin/activate
(.env) $ python -m pip install --upgrade pip
(.env) $ python -m pip install -r requirements.txt
(.env) $ properdocs serve
INFO    -  Building documentation...
INFO    -  Cleaning site directory
WARNING -  Doc file 'abc.md' contains a link 'xyz.md', but the
           target 'xyz.md' is not found among documentation files.
INFO    -  Documentation built in 3.30 seconds
# properdocs serve should update the site when source files are editted
INFO    -  [14:01:04] Watching paths for changes: 'docs', 'properdocs.yml'
# the site will be hosted locally on port 8000
INFO    -  [14:01:04] Serving on http://127.0.0.1:8000/bsp_tool_docs/
# Ctrl+C to kill the server
^CINFO    -  Shutting down...
(.env) $ exit
$
```
