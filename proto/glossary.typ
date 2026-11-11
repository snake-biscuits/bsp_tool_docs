= Glossary

== Branch Script
Python module detailing a branch's `.bsp` format variant.

Contains definitions for _LumpClasses_ & methods.


== BspClass
Subclass of ```python base.Bsp()```.

Container for _lumps_, branch methods & metadata.


== Lump
Block of data inside a `.bsp` file.

=== BasicLump
Array of common type. (i.e. ```C uint32_t```)

=== Lump
Array of ```C struct```.

=== SpecialLump
Complex data of variable length.


== LumpClass
Python implementation of a _lump's_ ```c struct```.


== Lump System
Collection of interconnected _lumps_.