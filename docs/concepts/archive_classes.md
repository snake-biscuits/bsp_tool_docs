# ArchiveClasses

`#!py ArchiveClasses` are subclasses of `#!py bsp_tool.archives.Archive`

They provide a means of navigating the filesystem inside an Archive
(inspecting folders & reading files)

Originally built to mimic `#!py zipfile.ZipFile`

Extended with some utilities inspired by the `#!py os.path` & `#!py fnmatch` modules



## Methods
### Initialisers
`#!py def from_file(cls, filename: str) -> Archive:`
:   open Archive from a file

`#!py def from_archive(cls, parent_archive: Archive, filename: str) -> Archive:`
:   open Archive from inside another Archive

`#!py def from_bytes(cls, raw_archive: bytes) -> Archive:`
:   open Archive from raw bytes

`#!py def from_stream(cls, stream: io.BytesIO) -> Archive:`
:   open Archive from a bytestream


### General Utilities
`#!py def namelist(self) -> List[str]:`
:   returns a list of all filenames present in the Archive

`#!py def read(self, filename: str) -> bytes:`
:   returns the raw bytes of `#!py filename`

`#!py def sizeof(self, filename: str) -> int:`
:   returns the length of `#!py filename` (in bytes)


### Path Utilities
`#!py def is_dir(self, filename: str) -> bool:`
:   returns `#!py True` if `#!py filename` is a folder inside the Archive

`#!py def is_path(self, filename: str) -> bool:`
:   returns `#!py True` if `filename` is a file inside the Archive

`#!py def path_exists(self, filename: str) -> bool:`
:   returns `#!py True` if `#!py filename` `#!py is_dir` or `#!py is_path`

`#!py def search(self, pattern="*.bsp", case_sensitive=False) -> List[str]:`
:   find all filenames matching `#!py pattern` in the Archive

`#!py def tree(self, folder: str = ".", depth: int = 0):`
:   pretty print contents of the Archive, starting at `#!py folder`


### Extraction
`#!py def extract(self, filename: str, to_path=None):`
:   write the contents of `#!py filename` to a file

`#!py def extract_all(self, to_path=None):`
:   run `#!py .extract()` on every file in `#!py Archive.namelist()`

`#!py def extract_all_matching(self, pattern="*.bsp", to_path=None, case_sensitive=False):`
:   run `#!py .extract()` on every file in `#!py Archive.search(pattern)`
