__all__ = [
    "utils",
    "branches", "bsps", "calendar", "engines", "timeline"]

from . import utils

from . import branches
from . import bsps
from . import calendar
from . import engines
from . import timeline


modules = [
    branches,
    bsps,
    calendar,
    engines,
    timeline]


def build():
    for module in modules:
        module.generate_all()
