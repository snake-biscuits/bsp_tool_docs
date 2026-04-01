# Portal Lumps

Diagrams & notes from the `respawn.titanfall` branch script:

```
       /-> Cells
      /--> Planes
Portal --> PortalEdgeReferences   -> PortalEdges -> PortalVertices
      \--> PortalVertexReferences -> PortalVertices
```

```
PortalVertexEdges -> PortalEdgeIntersectHeader -> PortalIntersectAtEdge   -> PortalEdges
                                              \-> PortalIntersectAtVertex -> PortalVertices
```

```
PortalVertexEdges is parallel w/ PortalVertices
```

```
PortalIntersectHeader is pseudo-parallel w/ PortalEdges (twice as many Edge as Header)
PortalEdgeReferences doesn't reference every entry in PortalEdges
Most PortalEdgeReferences entries are even, less are odd
```


## `PortalVertices`

Titanfall's `mp_angel_city` was very useful when reverse engineering the Portal system.
`Portals[0:3]` are a great sample set:

```python
>>> import bsp_tool
>>> bsp = bsp_tool.load_bsp("/home/bikkie/drives/ssd1/Mod/Titanfall/maps/mp_angel_city.bsp")
>>> bsp.PORTALS[:3]
[<Portal (is_reversed: 0, type: <PortalType.CELL: 0>, num_edges: 4, padding: 0, first_reference: 0, cell: 1, plane: 0)>,
 <Portal (is_reversed: 0, type: <PortalType.CELL: 0>, num_edges: 4, padding: 0, first_reference: 4, cell: 1, plane: 0)>,
 <Portal (is_reversed: 0, type: <PortalType.CELL: 0>, num_edges: 4, padding: 0, first_reference: 8, cell: 1, plane: 0)>]
```

We can get vertex loop by doing a `Portal->PortalVertRef->PortalVert` lookup:

```python
>>> # Portal[0] (A) 1>2>3>4
>>> [(i, bsp.PORTAL_VERTICES[i]) for i in bsp.PORTAL_VERTEX_REFERENCES[0:0+4]]
[(1, <Vertex (x: -17152.0, y: -17152.0, z: -2560.0)>),
 (2, <Vertex (x: -15872.0, y: -17152.0, z: -2560.0)>),
 (3, <Vertex (x: -15872.0, y: -15872.0, z: -2560.0)>),
 (4, <Vertex (x: -17152.0, y: -15872.0, z: -2560.0)>)]
>>> # Portal[1] (B) 5>6>7>8
>>> [(i, bsp.PORTAL_VERTICES[i]) for i in bsp.PORTAL_VERTEX_REFERENCES[4:4+4]]
[(5, <Vertex (x:  +7680.0, y: -17152.0, z: -2560.0)>),
 (6, <Vertex (x: +17152.0, y: -17152.0, z: -2560.0)>),
 (7, <Vertex (x: +17152.0, y: -15872.0, z: -2560.0)>),
 (8, <Vertex (x:  +7680.0, y: -15872.0, z: -2560.0)>)]
>>> # Portal[2] (C) 2>5>8>3
>>> [(i, bsp.PORTAL_VERTICES[i]) for i in bsp.PORTAL_VERTEX_REFERENCES[8:8+4]]
[(2, <Vertex (x: -15872.0, y: -17152.0, z: -2560.0)>),
 (5, <Vertex (x:  +7680.0, y: -17152.0, z: -2560.0)>),
 (8, <Vertex (x:  +7680.0, y: -15872.0, z: -2560.0)>),
 (3, <Vertex (x: -15872.0, y: -15872.0, z: -2560.0)>)]
```

Each portal touches at least one of the others, and they're all quads with right-angled corners.

```
1 > 2 > 5 > 6
^ A | C | B v
4 < 3 < 8 < 7
```

We can also see in this rough ASCII sketch that our portals have 2 edges in common:
 * `1>2>5>6` as our top edge
 * `4<3<8<7` as our bottom edge

> the orientation of this diagram is a guess, that will come up later

Note that we use a `|` character to diagram the `2-3` & `5-8` edges.
This is because they flow in both directions, depending on which portal "owns" the edge.


### `PortalVertex[0]`

The first `PortalVertex` is always the world origin, even if it isn't part of a portal.

```python
>>> bsp.PORTAL_VERTICES[0]
<Vertex (x: 0.0, y: 0.0, z: 0.0)>
```


## `PortalVertexEdges`

`PortalVertexEdges` is a lookup table to find edges containing each vertex
Since `PVE`s is parallel with `PortalVertices`, you use the index in `PortalVertices` to do lookups

The `IndexSet` is a variable length list (max 8 entries).
`-1` marks unused indices

> we skip `PVE[0]` here because it isn't referenced by any edges (all indices are `-1`)

```python
>>> {i+1: ves for i, ves in enumerate(bsp.PORTAL_VERTEX_EDGES[1:8+1])}
{1: PortalIndexSet(index=(0, 1, -1, -1, -1, -1, -1, -1)),
 2: PortalIndexSet(index=(1, 2, -1, -1, -1, -1, -1, -1)),
 3: PortalIndexSet(index=(2, 3, 33, -1, -1, -1, -1, -1)),
 4: PortalIndexSet(index=(0, 3, 36, -1, -1, -1, -1, -1)),
 5: PortalIndexSet(index=(4, 1, -1, -1, -1, -1, -1, -1)),
 6: PortalIndexSet(index=(1, 5, -1, -1, -1, -1, -1, -1)),
 7: PortalIndexSet(index=(5, 3, 41, -1, -1, -1, -1, -1)),
 8: PortalIndexSet(index=(4, 3, 31, -1, -1, -1, -1, -1))}
```

Taking our vertex loops from the `Portal->PortalVertexRefs->PortalVertices` lookup, we can see a pattern:

```
A: vert loop 1>2>3>4 => edge 0/1 > 1/2 > 2/3 > 3/0
B: vert loop 5>6>7>8 => edge 4/1 > 1/5 > 5/3 > 3/4
C: vert loop 2>5>8>3 => edge 2/1 > 1/4 > 4/3 > 3/2
```

Grouping pairs of common edges gives us a loop form we'd expect:
 * `a/b > b/c > c/d > d/a`

Luckily for us, the order of these groups highlights common edges.
All 3 portals touch edges 1 & 3 at the same point in sequence.


### Reverse `PortalVertexEdges` Lookup

First, we need a simpler `PVE` representation:

```python
>>> pve = {
...     vertex_index: {
...         edge_index
...         for edge_index in index_set.index
...         if edge_index != -1}
...     for vertex_index, index_set in enumerate(bsp.PORTAL_VERTEX_EDGES[:9])}
```

Inverting the `Vertex->Edge` mapping into `Edge->Vertex`:

```
>>> {i: {vi for vi, eis in pve.items() if i in eis} for i in range(6)}
{0: {1, 4},
 1: {1, 2, 5, 6},  # top edge
 2: {2, 3},
 3: {3, 4, 7, 8},  # bottom edge
 4: {5, 8},
 5: {6, 7}}
```

Now we can see which edges each `PortalVertex` lies on:

```
a 1 b 1 e 1 f
0 A 2 C 4 B 5
d 3 c 3 h 3 g
```

> lowercase: `PortalVertices`, uppercase: `Portal`, numbers: `PortalEdges`

So there's one major thing we can take from this:
 * **An edge can contain multiple points, not just a start & end**

> in fact, in `mp_angel_city` an edge can be shared by up to 20 points

However, `PortalEdges` is still only pairs or points, what's going on there?


## Edge Groups

Each of the shared edges have the same value along 2 axes.
Filtering `PortalVertices`, we get these points along each edge:

```python
>>> {i: v for i, v in enumerate(bsp.PORTAL_VERTICES) if v.y == -17152 and v.z == -2560}
{ 1: <Vertex (x: -17152.0, y: -17152.0, z: -2560.0)>,
  2: <Vertex (x: -15872.0, y: -17152.0, z: -2560.0)>,
  5: <Vertex (x:  +7680.0, y: -17152.0, z: -2560.0)>,
  6: <Vertex (x: +17152.0, y: -17152.0, z: -2560.0)>}
>>> {i: v for i, v in enumerate(bsp.PORTAL_VERTICES) if v.y == -15872 and v.z == -2560}
{ 3: <Vertex (x: -15872.0, y: -15872.0, z: -2560.0)>,
  4: <Vertex (x: -17152.0, y: -15872.0, z: -2560.0)>,
  7: <Vertex (x: +17152.0, y: -15872.0, z: -2560.0)>,
  8: <Vertex (x:  +7680.0, y: -15872.0, z: -2560.0)>,
 45: <Vertex (x:  +8192.0, y: -15872.0, z: -2560.0)>,
 53: <Vertex (x: +15872.0, y: -15872.0, z: -2560.0)>}
```

Our bottom edge extends all the way out to `PortalVertex[53]` at the `+X` end

> this will come up again when we discuss `PEIV`

```python
>>> {i: bsp.PORTAL_EDGES[i*2:(i+1)*2] for i in range(6)}
{0: [35,  1],
 1: [ 1,  6],
 2: [ 2, 37],
 3: [ 7,  4],
 4: [34,  5],
 5: [ 6, 54]}
```


## `PortalEdges`

By far the most confusing to reverse, `PortalEdges` functions unlike any other lump.
It contains pairs of indices, and either member of that pair in indexed individually.
(at least, when the index if coming from `PortalEdgeRefs`)

There are twice as many entries in `PortalEdges` as `PortalEdgeIntersectHeaders`.
Meaning they are parallel, when you recognise that a **pair of indices** is **one** `PortalEdge`.

### `PortalVertex, PortalEdge->PortalVertex` pairs

Just for fun, let's try looking at `PortalVertRefs` & `PortalEdgeRefs` together:

```python
>>> [  # Portal[0] (A)
...     (i, bsp.PORTAL_VERTICES[i], j, bsp.PORTAL_VERTICES[bsp.PORTAL_EDGES[j]])
...     for i, j in zip(bsp.PORTAL_VERTEX_REFERENCES[0:0+4], bsp.PORTAL_EDGE_REFERENCES[0:0+4])]
[(1, <Vertex (x: -17152.0, y: -17152.0, z: -2560.0)>, 35, <Vertex (x: -17152.0, y: +17152.0, z: -2560.0)>),
 (2, <Vertex (x: -15872.0, y: -17152.0, z: -2560.0)>,  1, <Vertex (x: -17152.0, y: -17152.0, z: -2560.0)>),
 (3, <Vertex (x: -15872.0, y: -15872.0, z: -2560.0)>,  2, <Vertex (x: -15872.0, y: -17152.0, z: -2560.0)>),
 (4, <Vertex (x: -17152.0, y: -15872.0, z: -2560.0)>,  7, <Vertex (x: +17152.0, y: -15872.0, z: -2560.0)>)]
```

So these indices make 0 sense.
My expectation is edges should enclose the portal shape described by the `PortalVertex` loop.
But we have 2 `PortalVertex` indices here that aren't part of `Portal[0]`.

Extending our Portal A diagram to include these points, we get this shape:

```
   35
    ^
    1 < 2
      A ^
7 < 4   3
```

However, these vertex positions are guesses.
When we use the actual positions:

```
35
 ^
 4 - 3 > 7
 | A v
 1 < 2
```

`PortalEdges` do actually enclose the `PortalVertex` loop as we'd expect!
Only the start & end points of the edge are stored in the lump, so edges extend out like this.
Trimmed to fit the `Portal`, we get:

```
4 < 3
v A ^
1 > 2
```

`PV, PE->PV` pairs flow the opposite direction to the `PortalVertex` loop.

> `PV, PE->PV` pairs are an arbitrary structure.
> Nothing was found to indicate the game engine interprets data in this way.
> We are assuming this observation holds true consistently across all `Portals`.
> We have not tested this assumption.


## `PortalEdgeIntersect`

`PortalEdgeIntersectHeader` is parallel with `PortalEdges` (as pairs)
`Headers` index into either `PortalEdgeIntersectEdge` or `PortalEdgeIntersectVertex`

Both lumps consist of `IndexSets`, a sort of variable length list

From analysing the ranges of the indices in these index sets, we ca assume:
 * `PEIE` indexes into `PortalEdges` (as pairs)
 * `PEIV` indexes into `PortalVertices`

```python
>>> [bsp.PORTAL_EDGE_INTERSECT_AT_VERTEX[h.start:h.start+h.count] for h in bsp.PORTAL_EDGE_INTERSECT_HEADER[:6]]
[[PortalIndexSet(index=(1, 4, 36, 35, 4, 36, -1, -1))],
 [PortalIndexSet(index=(1, 2, 5, 6, -1, -1, -1, -1))],
 [PortalIndexSet(index=(2, 3, 37, 3, 37, -1, -1, -1))],
 [PortalIndexSet(index=(4, 3, 8, 7, 45, 53, 8, 3)), PortalIndexSet(index=(4, 53, 45, 7, -1, -1, -1, -1))],
 [PortalIndexSet(index=(5, 8, 33, 34, 41, 42, 58, 8)), PortalIndexSet(index=(41, 33, 34, -1, -1, -1, -1, -1))],
 [PortalIndexSet(index=(6, 7, 54, 50, 51, 7, -1, -1))]]
>>> [bsp.PORTAL_EDGE_INTERSECT_AT_EDGE[h.start:h.start+h.count] for h in bsp.PORTAL_EDGE_INTERSECT_HEADER[:6]]
[[PortalIndexSet(index=(1, 3, 18, 19, 36, 636, -1, -1))],
 [PortalIndexSet(index=(0, 2, 4, 5, -1, -1, -1, -1))],
 [PortalIndexSet(index=(1, 3, 18, 33, 46, -1, -1, -1))],
 [PortalIndexSet(index=(0, 2, 4, 5, 22, 24, 31, 33)), PortalIndexSet(index=(36, 37, 40, 41, -1, -1, -1, -1))],
 [PortalIndexSet(index=(1, 3, 18, 19, 20, 21, 25, 31)), PortalIndexSet(index=(42, 45, 988, -1, -1, -1, -1, -1))],
 [PortalIndexSet(index=(1, 3, 19, 21, 25, 41, -1, -1))]]
```

Stripping out the syntax so we can focus on the indices:

```python
PortalEdgeIntersectAtVertex 0..5
  1   4  36  35   4  36
  1   2   5   6 
  2   3  37   3  37 
  4   3   8   7  45  53   8   3   4  53  45  7
  5   8  33  34  41  42  58   8  41  33  34
  6   7  54  50  51   7

PortalEdgeIntersectAtEdge 0..5
  1   3  18  19  36 636
  0   2   4   5 
  1   3  18  33  46
  0   2   4   5  22  24  31  33  36  37  40  41
  1   3  18  19  20  21  25  31  42  45 988
  1   3  19  21  25  41
```

Note how `PEIV[1]` & `PEIV[3]` line up with the edge groups we found earlier by filtering `PortalVerts`

> TODO: remark on duplicates in `PEIV` & lack of duplicates in `PEIE`
> TODO: remark on PEIV & PEIE sets being the same length
> TODO: investigate relationship, are `PEIV`-`PEIE` pairs significant?

> TODO: diagram out all 3 portals, using the all edges
> -- this should also help us validate PEIV & see the PEIE relationship
