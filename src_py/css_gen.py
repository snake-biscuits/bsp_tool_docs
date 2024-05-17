# TODO: generate css
# -- some will be per page type
# -- try to be modular (multiple stylesheets per page)
# -- something like MediaWiki templates
from typing import Dict



class StyleSheet:
    classes: Dict[str, StyleClass]
    ...


class StyleClass:
    rules: Dict[str, str]
    ...
