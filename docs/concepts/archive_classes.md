# ArchiveClasses

`ArchiveClasses` are based on `bsp_tool.archives.Archive`

They provide a means of navigating the filesystem inside an Archive
(inspecting folders & reading files)

Originally built to mimic `zipfile.ZipFile`

Extended with some utilities inspired by the `os.path` & `fnmatch` modules



## Methods
### Initialisers
`#!python def from_file(cls, filename: str) -> Archive:`
:   open Archive from a file

`#!python def from_archive(cls, parent_archive: Archive, filename: str) -> Archive:`
:   open Archive from inside another Archive

`#!python def from_bytes(cls, raw_archive: bytes) -> Archive:`
:   open Archive from raw bytes

`#!python def from_stream(cls, stream: io.BytesIO) -> Archive:`
:   open Archive from a bytestream


### General Utilities
`#!python def namelist(self) -> List[str]:`
:   returns a list of all filenames present in the archive

`#!python def read(self, filename: str) -> bytes:`
:   returns the raw bytes of `filename`

`#!python def sizeof(self, filename: str) -> int:`
:   returns the length of `filename` (in bytes)


### Path Utilities
`#!python def is_dir(self, filename: str) -> bool:`
:   returns `True` if `filename` is a folder inside `Archive`

`#!python def is_path(self, filename: str) -> bool:`
:   returns `True` if `filename` is a file inside `Archive`

`#!python def path_exists(self, filename: str) -> bool:`
:   returns `True` if `filename` `is_dir` or `is_path`

`#!python def search(self, pattern="*.bsp", case_sensitive=False) -> List[str]:`
:   find all filenames matching `pattern` in `Archive`

`#!python def tree(self, folder: str = ".", depth: int = 0):`
:   pretty print contents of `Archive` starting at `folder`


### Extraction
`#!python def extract(self, filename: str, to_path=None):`
:   write the contents of `filename` to a file in the working directory (or `to_path`)

`#!python def extract_all(self, to_path=None):`
:   run `.extract()` on every file in `Archive.namelist()`

`#!python def extract_all_matching(self, pattern="*.bsp", to_path=None, case_sensitive=False):`
:   run `.extract()` of every file in `Archive.search(pattern)`
