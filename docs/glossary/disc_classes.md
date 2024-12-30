# DiscClasses

`DiscClasses` are subclasses of `bsp_tool.archives.DiscImage`

They emulate a CD-ROM disc image

Unlike [`ArchiveClasses`](archive_classes.md), they do not expose filesystems

Though individual [CD-DA](https://en.wikipedia.org/wiki/Compact_Disc_Digital_Audio) tracks can be exported as `.wav` files



## Reading files
Discs can contain [ISO-9660](https://www.iso.org/obp/ui/en/#iso:std:iso-iec:9660:ed-1:v1:en) / [ECMA-119](https://ecma-international.org/publications-and-standards/standards/ecma-119/) filesystems

These can be parsed with the [`cdrom.Iso`](../archives/cdrom/Iso.md) [ArchiveClass](archive_classes.md)



## Methods
### Initialisers
`#!python def from_archive(cls, parent_archive: Archive, filename: str) -> DiscImage:`
:   opens Disc from [Archive](archive_classes.md)


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
