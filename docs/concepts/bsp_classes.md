# BspClasses

`BspClasses` are based on `bsp_tool.base.Bsp`

They provide a container for lumps & metadata



## Methods
### Initialisers
`#!python def from_file(cls, branch: ModuleType, filepath: str) -> Bsp:`
:   open Bsp from file

`#!python def from_archive(cls, branch: ModuleType, filepath: str, parent_archive) -> Bsp:`
:   open Bsp from inside [Archive](archive_classes.md)

`#!python def from_bytes(cls, branch: ModuleType, filepath: str, raw_bsp: bytes) -> Bsp:`
:   open Bsp from raw bytes

`#!python def from_stream(cls, branch: ModuleType, filepath: str, stream: io.BytesIO) -> Bsp:`
:   open Bsp from a bytestream

<!-- TODO: uncomment when it's actually a feature
### General Utilities
`#!python def save(self):`
:   save edits made to Bsp
    writes to `Bsp.folder`/`Bsp.filename`
-->

### Branch Methods
When initialised, methods defined in `branch` are attached to the `Bsp`.
These methods 
