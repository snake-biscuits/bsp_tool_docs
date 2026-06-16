# Systems


> parallel means entries with the same index are paired across lumps
> this allows splitting "object" to be used by 2 systems independantly
> but this does increase the odds of storing redundant data


## Lighting
### Cascading Shadow Maps
```
CSMAABBNode -> CSMObjReference -> ??? (starts high, out of ObjRefs range)
           \-> CSMAABBNode
```

### Lightmaps
```
LightmapHeader -> LIGHTMAP_DATA_SKY
              \-> LIGHTMAP_DATA_REAL_TIME_LIGHTS
```

### Lightprobes
```
LightProbeTree -?> LightProbeRef -> LightProbe
StaticPropLightProbeIndices & StaticProps are parallel
```

### Shadow Meshes
```
ShadowMesh -> ShadowMeshIndex -> ShadowMeshOpaqueVertex
          \-> MaterialSort?  \-> ShadowMeshAlphaVertex
```

### Worldlights
```
Worldlights
```

> connects to more lumps in later branches



## Visibility
### ObjReferences

> might fit better under rendering?

```
CellAABBNodes -> ObjReferences -> Meshes / StaticProp
             \-> CellAABBNodes
```
```
ObjReferences indices start w/ Model[0] (worldspawn) meshes, then GameLump.sprp.props
ObjReferences & ObjReferenceBounds are parallel
```

### Cells

[cells](cells.md)


### Portals

[portals](portals.md)


## Physics

### Clip Model

Main Physics Lookup Tree

> `CM_*` is probably short for Clip Model
> This terminology is used in Quake3's source code

> `CM_GRID` holds world bounds & other metadata

> TODO: CM_Grid / clip_model system page
> -- each primitive type is basically a system
> -- Brushes, Tricoll & StaticProps (Titanfall 2 PrimitiveType)

```
Grid -> GridCell -> GeoSet -> Primitive
```
```
         /-> UniqueContents
Primitive -> .primitive.type / .type -> Brush OR Tricoll
```
```
GeoSets can contain duplicates (use same .straddle_group)
GeoSets is parallel w/ GeoSet Bounds
Primitives is parallel w/ PrimitiveBounds
PrimitiveBounds & GeoSetBounds use the same "Bounds" type
```

### Brushwork
```
     /-> BrushSidePlaneOffset -> Plane
Brush -> BrushSideProperties -> TextureData
     \-> BrushSideTextureVector
```
```
BrushSideProperties is parallel w/ BrushSideTextureVector (one per brushside)
len(BrushSideProperties/TextureVectors) = len(Brushes) * 6 + len(BrushSidePlaneOffsets)
Brush.num_brush_sides (derived) is 6 + Brush.num_plane_offsets
```

### TriColl

Triangle Collision for patches, displacements & models converted to `.bsp` geo

```
             /-> TextureData
            /--> Vertices
TricollHeader -> TricollTriangle -> Vertices
            \--> TricollNode -?> TricollNode / ???
             \-> TricollBevelIndices? -?> ?

TricollBevelStarts is parallel w/ TricollTriangles
```


## Rendering
### Models
```
             /-> MaterialSort -> TextureData -> TextureDataStringTable -> TextureDataStringData
Model -> Mesh -> MeshIndex -\-> VertexReservedX -> Vertex
            \--> .flags (VertexReservedX)     \--> VertexNormal
             \-> VertexReservedX               \-> .uv

MeshBounds & Mesh are parallel
```
