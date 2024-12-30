# BspClasses

`BspClasses` are subclasses of `base.Bsp`

They provide a container for lumps & metadata



## Methods
### Initialisers
`#!py def from_file(cls, branch: ModuleType, filepath: str) -> Bsp:`
:   open Bsp from file

`#!py def from_archive(cls, branch: ModuleType, filepath: str, parent_archive) -> Bsp:`
:   open Bsp from inside an [ArchiveClass](archive_classes.md)

`#!py def from_bytes(cls, branch: ModuleType, filepath: str, raw_bsp: bytes) -> Bsp:`
:   open Bsp from raw bytes

`#!py def from_stream(cls, branch: ModuleType, filepath: str, stream: io.BytesIO) -> Bsp:`
:   open Bsp from a bytestream

<!-- TODO: uncomment when it's actually a feature
### General Utilities
`#!py def save(self):`
:   save edits made to Bsp
    writes to `Bsp.folder`/`Bsp.filename`

`#!py def save_as(self, filename: str):`
:   same as `#!py .save()`, but writes to `#!py filename`
-->

### Branch Methods
`BspClasses` cannot be initialised without a [BranchScript](branch_scripts.md).
During initialisation the `#!py methods` of the BranchScript are attached to the Bsp.

These methods expect a specific `.bsp` format, but can be shared between branches.
Many are essentially macros for common operations (e.g. looking up a texture name).
Some are more advanced (e.g. converting a level segment to a generic 3D model).
