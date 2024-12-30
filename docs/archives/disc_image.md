# `archives.DiscImage`

Base class of all [DiscClasses](../glossary/disc_classes.md)


## Methods
### Initialisers
`#!python def from_archive(cls, parent_archive: Archive, filename: str) -> DiscImage:`
:   opens Disc from [ArchiveClass](../glossary/archive_classes.md)


### General Utilities
`#!python def export_wav(self, track_index: int, filename: str = None):`
:   write the indexed track to `filename` as a `.wav`, if it's audio

`#!python def read(self, length: int = -1) -> bytes:`
:   reads `length` bytes, starting at the current sector
    will advance the "cursor" by whole sectors

`#!python def sector_read(self, length: int = -1) -> bytes:`
:   reads `length` sectors (sets of 2048 bytes)

`#!python def sector_seek(self, lba: int, whence: int = 0) -> int:`
:   seeks to sector `lba` (Logical Block Address)
    `whence = 0`: relative to start of disc
    `whence = 1`: relative to current sector
    `whence = 2`: relative to end of disc

`#!python def sector_tell(self) -> int:`
:   returns the current `lba`
