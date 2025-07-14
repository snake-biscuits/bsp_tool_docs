# `base.Bsp`

## Methods
### Initialisers
...

### Utilities
`#!py def lump_as_bytes(self, lump_name: str) -> bytes:`
:   convert the named lump back into bytes


### External File Linking
`#!py def extra_patterns(self) -> List[str]:`
:   returns a list of `fnmatch` patterns for filenames to mount

`#!py def mount_file(self, filename: str, external_file: external.File):`
:   mount an external file onto `self.extras`

`#!py def unmount_file(self, filename: str):`
:   unmount an external file from `self.extras`
