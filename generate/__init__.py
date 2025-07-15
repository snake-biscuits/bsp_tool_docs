__all__ = [
    "utils",
    "branches", "bsps", "engines"]

from . import utils

from . import branches
from . import bsps
from . import engines


modules = [
    branches,
    bsps,
    engines]


def build():
    for module in modules:
        module.generate_all()
