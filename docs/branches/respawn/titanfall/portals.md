# Portal Lumps

```
       /-> Cells
      /--> Planes
Portal --> PortalEdgeReferences   -> PortalEdges -> ???
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
PortalEdgeReferences doesn't presicely index all edges (can be short by one)
Most PortalEdgeReferences entries are even, less are odd
```

> NOTE: Python samples are from exploring `Titanfall/maps/mp_angel_city.bsp`


## PortalVertices
```python
>>> import bsp_tool
>>> bsp = bsp_tool.load_bsp("/home/bikkie/drives/ssd1/Mod/Titanfall/maps/mp_angel_city.bsp")
>>> bsp.PORTAL_VERTICES[0]
<Vertex (x: 0.0, y: 0.0, z: 0.0)>  # alway 0,0,0
>>> bsp.PORTALS[:4]
[<Portal (is_reversed: 0, type: <PortalType.CELL: 0>, num_edges: 4, padding: 0, first_reference: 0, cell: 1, plane: 0)>,
 <Portal (is_reversed: 0, type: <PortalType.CELL: 0>, num_edges: 4, padding: 0, first_reference: 4, cell: 1, plane: 0)>,
 <Portal (is_reversed: 0, type: <PortalType.CELL: 0>, num_edges: 4, padding: 0, first_reference: 8, cell: 1, plane: 0)>,
 <Portal (is_reversed: 0, type: <PortalType.CELL: 0>, num_edges: 4, padding: 0, first_reference: 12, cell: 6, plane: 1)>]
>>> [bsp.PORTAL_VERTICES[i] for i in (1, 2, 3, 4)]
[<Vertex (x: -17152.0, y: -17152.0, z: -2560.0)>,
 <Vertex (x: -15872.0, y: -17152.0, z: -2560.0)>,
 <Vertex (x: -15872.0, y: -15872.0, z: -2560.0)>,
 <Vertex (x: -17152.0, y: -15872.0, z: -2560.0)>]
>>> [bsp.PORTAL_VERTICES[i] for i in (5, 6, 7, 8)]
[<Vertex (x: 7680.0, y: -17152.0, z: -2560.0)>,
 <Vertex (x: 17152.0, y: -17152.0, z: -2560.0)>,
 <Vertex (x: 17152.0, y: -15872.0, z: -2560.0)>,
 <Vertex (x: 7680.0, y: -15872.0, z: -2560.0)>]
>>> [bsp.PORTAL_VERTICES[i] for i in (2, 5, 8, 3)]
[<Vertex (x: -15872.0, y: -17152.0, z: -2560.0)>,
 <Vertex (x: 7680.0, y: -17152.0, z: -2560.0)>,
 <Vertex (x: 7680.0, y: -15872.0, z: -2560.0)>,
 <Vertex (x: -15872.0, y: -15872.0, z: -2560.0)>]
>>> [bsp.PORTAL_VERTICES[i] for i in (9, 10, 11, 12)]
[<Vertex (x: 3192.0, y: 3568.0, z: -2048.0)>,
 <Vertex (x: 3192.0, y: -3200.0, z: -2048.0)>,
 <Vertex (x: -3496.0, y: -3200.0, z: -2048.0)>,
 <Vertex (x: -3496.0, y: 3568.0, z: -2048.0)>]
```
```
1 > 2 > 5 > 6
^ A | C | B v
4 < 3 < 8 < 7
```


## PortalVertexEdges
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
using vertex loops from `Portal->PortalVertexRefs->PortalVertices`:
```
A: edge 0/1-1/2-2/3-3/0 (vert 1-2-3-4)
B: edge 4/1-1/5-5/3-3/4 (vert 5-6-7-8)
C: edge 2/1-1/4-4/3-3/2 (vert 2-5-8-3)
```
these sequences describe loops of edges around quads: `a/b-b/c-c/d-d/a`

the numbers inside each index sets appear to be edges
we used them to index PortalEdgeIntersectheader


### Interconnect
```python
>>> {
...     i: [
...         j
...         for j, pev in enumerate(bsp.PORTAL_VERTEX_EDGES)
...         if i in pev.index]
...     for i in range(4)}
{0: [ 1,  4, 35, 36],
 1: [ 1,  2,  5,  6],
 2: [ 2,  3, 37],
 3: [ 3,  4,  7,  8, 45, 53]}
```
```python
>>> max(
...     len([
...         j
...         for j, pev in enumerate(bsp.PORTAL_VERTEX_EDGES)
...         if i in pev.index])
...     for i, _ in enumerate(bsp.PORTAL_VERTEX_EDGES))
20
```
edges can contain up to 20 vertices
not just point A to B, as assumed previously


## PortalEdgeIntersectHeader
PortalIntersectHeader connects ?edges? to multiple IndexSets
This allows for multiple connections per ?edge?

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


## PortalEdges
first 3 portals, 4 refs each
vertex refs on the left
edge refs on the right
```
  verts | edges
1 2 3 4 | 0 2 4 6
5 6 7 8 | 8 2 A 6
2 5 8 3 | 5 2 9 6
```
all 3 portals share edges 2 & 6
those edges must contain the full set of vertices along each edge
```
1 > 2 > 5 > 6
^ A | C | B v
4 < 3 < 8 < 7
```
so we need the sets `{1, 2, 5, 6}` & `{3, 4, 7, 8}`
from looking at `PortalVerts[1:9]`, we know these edges:
```python
>>> {i: v for i, v in enumerate(bsp.PORTAL_VERTICES) if v.y == -17152 and v.z == -2560}
{1: <Vertex (x: -17152.0, y: -17152.0, z: -2560.0)>,
 2: <Vertex (x: -15872.0, y: -17152.0, z: -2560.0)>,
 5: <Vertex (x: 7680.0, y: -17152.0, z: -2560.0)>,
 6: <Vertex (x: 17152.0, y: -17152.0, z: -2560.0)>}
>>> {i: v for i, v in enumerate(bsp.PORTAL_VERTICES) if v.y == -15872 and v.z == -2560}
{3: <Vertex (x: -15872.0, y: -15872.0, z: -2560.0)>,
 4: <Vertex (x: -17152.0, y: -15872.0, z: -2560.0)>,
 7: <Vertex (x: 17152.0, y: -15872.0, z: -2560.0)>,
 8: <Vertex (x: 7680.0, y: -15872.0, z: -2560.0)>,
 45: <Vertex (x: 8192.0, y: -15872.0, z: -2560.0)>,
 53: <Vertex (x: 15872.0, y: -15872.0, z: -2560.0)>}
```
and we also found more vertices along the same edge
all vertex indices in these sets can be found in `PEIaV` entries 1 & 3
but now what? how do `PortalEdgeReferences` & `PortalEdges` work? **idk**


## Fish Shapes
```python
>>> bsp.PORTAL_VERTEX_EDGES[1:8+1]
[PortalIndexSet(index=(0, 1, -1, -1, -1, -1, -1, -1)),
 PortalIndexSet(index=(1, 2, -1, -1, -1, -1, -1, -1)),
 PortalIndexSet(index=(2, 3, 33, -1, -1, -1, -1, -1)),
 PortalIndexSet(index=(0, 3, 36, -1, -1, -1, -1, -1)),
 PortalIndexSet(index=(4, 1, -1, -1, -1, -1, -1, -1)),
 PortalIndexSet(index=(1, 5, -1, -1, -1, -1, -1, -1)),
 PortalIndexSet(index=(5, 3, 41, -1, -1, -1, -1, -1)),
 PortalIndexSet(index=(4, 3, 31, -1, -1, -1, -1, -1))]
```
```
     0 - 1
     |   |
33 - 3 - 2
     |
    36
```
```
     4 - 1
     |   |
41 - 3 - 5
     |
    31
```
these "edges" don't link up like we'd expect our 3 portals to
probably got their representations wrong
is this the derivative of a node-graph?

yeah nah, hard misread here
`PortalVertexEdges[vertex_index] => [edge_index, ...]`
the fish are indeed node-graphs, but broken
we've found a way to represent the vertices as edges
