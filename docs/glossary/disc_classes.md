# DiscClasses

DiscClasses are subclasses of [`archives.DiscImage`](../archives/disc_image.md)

They emulate a CD-ROM disc image

Unlike [ArchiveClasses](archive_classes.md), they do not expose filesystems

Though individual [CD-DA](https://en.wikipedia.org/wiki/Compact_Disc_Digital_Audio) tracks can be exported as `.wav` files


## Reading files
Discs can contain [ISO-9660](https://www.iso.org/obp/ui/en/#iso:std:iso-iec:9660:ed-1:v1:en) / [ECMA-119](https://ecma-international.org/publications-and-standards/standards/ecma-119/) filesystems

These can be parsed with the [`cdrom.Iso`](../archives/cdrom/Iso.md) [ArchiveClass](archive_classes.md)
