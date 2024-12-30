# BranchScripts

BranchScripts describe the data-structures of specific `.bsp` format variants.
They provide [BspClasses](bsp_classes.md) with [LumpClasses](lump_classes.md).
Besides parsing bytes, they also attach methods to the `Bsp` for easier processing.
Methods can be used for anything from getting texture names to exporting 3D models.

If you're looking for a specific BranchScript, [start here](../branches/index.md)


## Broad Structure
> TODO: break down the layout of a BranchScript, section by section

> -- should be equal parts of explaining how to read & write a BranchScript

 - [ ] Metadata
     - [ ] references in comments at top of file
     - [ ] `BSP_VERSION` & `FILE_MAGIC`
     - [ ] `GAME_PATHS` & `GAME_VERSIONS`
 - [ ] Enums
     - [ ] `LUMP`
     - [ ] Various Flags
     - [ ] Limits (some arbitrary, some inherent to the format)
 - [ ] Systems map (lump relationship notes)
 - [ ] LumpClasses


## Quake-Based Example

```python title="id_software/quake.py"
import enum

from .. import base
from ..utils import vector


BSP_VERSION = 29
FILE_MAGIC = None


class LUMP(enum.Enum):
    ENTITIES = 0
    ...
    VERTICES = 3
    ...


# LumpClasses, in alphabetical order
class Vertex(base.Struct, vector.vec3):
    __slots__ = [*"xyz"]
    _format = "3f"


LUMP_CLASSES = {
    "VERTICES": Vertex}


methods = dict()
```
