# `developer.branch` "LumpName" [lump index/id]

## C++

> Relevant types (related Enum, IntFlag & others)
> `utils` conversion (e.g. `physics.AABB`, `texture.TextureVector`)
> common `_classes` (e.g. `vector.vec3`)

```c++
typedef uint16_t LumpName;  /* BasicLumpClass */

struct LumpName {
    /* LumpClass */
};

void* LumpName(char* raw_data) {
    /* SpecialLumpClass */
}
```

> If we're doing our own syntax highlighted code blocks, make members into links

## Based on

 * Baseclass (how do we look that up? `inspect`?)
   - `base.MappedArray` etc.
   - parent branches' LumpClass

## Indexes

 * Other LumpClasses (in same `developer.branch`)

## Indexed by

 * Other LumpClasses (in same `developer.branch`)

## Related to

 * Alternate version (if Source-based)
 * Other LumpClasses (in different `developer.branch`)
