# Cell Lumps

> NOTE: unsure if CellAABBNodes are connected
> -- it'd make sense, but there's no indices afaik

Diagrams & notes from the `respawn.titanfall` branch script:

```
CellBspNode -> CellBspNode / Cell
           \-> Plane
```
```
Cell -> LeafWaterData -> TextureData (water material)
    \-> Portal
```

## CellBspNode

`CellBspNodes` is a tree, starting from index 0.
When the `.plane` index is `-1`, `.child` is a leaf `Cell`.
Otherwise, `CellBspNode[index+0]` or `index+1` is the next node.
If we want to be "in front" of the plane, we go to `index+0`.
This is difficult to understand without a visualisation.

> TODO: pull screenshots from research thread, w/ annotations


## Cell

Cells are essentially a collection of portals & some flags.
These flags tell the engine if the cell touches water or sky.
Portals can be used to traverse from one cell to another.
No precalculated PVS/PAS tables appear to exist.
It's unclear how exactly the game engine uses Cells for VIS.


## Planes

The `Plane` lump is only indexed by 2 lumps.
`CellBspNodes` & `CMBrushSidePlaneOffsets`
`CMGrid` contains a base offset into `Planes`.

VIS `Planes` appear first, and are often axis-aligned.
`Brush` planes consume the rest of the lump, and are never axis-aligned.
Some `Brushes` will index planes in the VIS section.

We can assume from this that some VIS calculations are performed before brushes are written.
Brushes are largely used for physics (within the [`CM_*` system](clip_model.md)).
Doing VIS first can help eliminate unseen faces for `Mesh` construction.
`CellAABBNodes` & `ObjRefs` counts should be greatly reduced by VIS optimisations.
