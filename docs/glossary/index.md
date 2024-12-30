# Glossary


## [ArchiveClass](archive_classes.md)

Virtual filesystem for accessing files inside archives (e.g. `.zip`)


## [BranchScript](branch_scripts.md)

Scripts which describe the format of a specific variant of the `.bsp` format.
Extends a parent [BspClass](#) with branch-specific methods & [LumpClass](#)es.


## [BspClass](bsp_classes.md)

How `bsp_tool` opens `.bsp` files.
Uses [BranchScript](#)s to make `.bsp` data a little more human-readable.


## [DiscClass](disc_classes.md)

Virtual disc-image.
Some [ArchiveClass](#)es can be initialised from disc-images.


## [Lump](lump.md)

Lumps are blocks of data stored in `.bsp`s.
Most lumps contain the same data-structure repeated over & over.
There's some nuance to it, but that's the gist.


## [LumpClass](lump_classes.md)

A "Pythonic" representation of `.bsp` data-structures.
Handles conversion to & from bytes, among other features.
