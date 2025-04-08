# Systems

## Worldspawn

<div class="svg-wrapper">
  <svg viewBox="0 0 512 64" xmlns="http://www.w3.org/2000/svg" xmlns:xhtml="http://www.w3.org/1999/xhtml">
    <path d="M 132 16 C 140 24, 128 48, 142 48"/>
    <path d="M 56 16 L 328 16"/>
    <foreignObject x="16" y="8" width="256" height="32">
      <a class="node">Entity</a>
    </foreignObject>
    <foreignObject x="76" y="8" width="256" height="32">
      <a class="node">Model</a>
    </foreignObject>
    <foreignObject x="140" y="8" width="256" height="32">
      <a class="node">Node</a>
    </foreignObject>
    <foreignObject x="196" y="8" width="256" height="32">
      <a class="node">Leaf</a>
    </foreignObject>
    <foreignObject x="248" y="8" width="256" height="32">
      <a class="node">LeafFace</a>
    </foreignObject>
    <foreignObject x="324" y="8" width="256" height="32">
      <a class="node">Face</a>
    </foreignObject>
    <path d="M 160 48 L 224 48"/>
    <foreignObject x="140" y="40" width="256" height="32">
      <a class="node">ClipNode</a>
    </foreignObject>
    <foreignObject x="216" y="40" width="256" height="32">
      <a class="node">Plane</a>
    </foreignObject>
  </svg>
</div>


## Visibility

<div class="svg-wrapper">
  <svg viewBox="0 0 512 64" xmlns="http://www.w3.org/2000/svg" xmlns:xhtml="http://www.w3.org/1999/xhtml">
    <path d="M 56 16 L 320 16"/>
    <foreignObject x="16" y="8" width="256" height="32">
      <a class="node">Visibility</a>
    </foreignObject>
    <foreignObject x="92" y="8" width="256" height="32">
      <a class="node">Node</a>
    </foreignObject>
    <foreignObject x="152" y="8" width="256" height="32">
      <a class="node">Leaf</a>
    </foreignObject>
    <foreignObject x="204" y="8" width="256" height="32">
      <a class="node">LeafFace</a>
    </foreignObject>
    <foreignObject x="280" y="8" width="256" height="32">
      <a class="node">Face</a>
    </foreignObject>
    <path d="M 144 16 C 152 24, 140 48, 154 48"/>
    <foreignObject x="152" y="40" width="256" height="32">
      <a class="node">Plane</a>
    </foreignObject>
  </svg>
</div>


## Faces
```
    /-> TextureInfo -> MipTextures -> MipTexture
Face -> SurfEdge -> Edge -> Vertex
   \--> Lightmap
    \-> Plane
```
