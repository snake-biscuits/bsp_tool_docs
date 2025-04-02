# Respawn Entertainment

Respawn Entertainment was founded by former Infinity Ward members.
Their version of the Source Engine was forked around 2011 from Portal 2.

> TODO: citations needed

While some remnants of the 2013 Source SDK remain, much is brand new.
(though similarities to CoD 2 & CoD 4's formats exist in Titanfall).

> TODO: give examples of the similarities.
> e.g. *unused* lump count in bsp header similar to modern warfare

## Founding
Respawn Entertainment was formed by Infinity Ward employees circa 2010.
For more details, read the page for [Infinity Ward](../infinity_ward/index.md)


## `.bsp` Spec
The Titanfall Engine has `rBSP` file-magic & 128 lumps.
Approximately 72 of the 128 possible lumps appear in `.bsp_lump` files.
The naming convention for `.bsp_lump` files is: `<bsp.filename>.<LUMP_HEX_ID>.bsp_lump`.
Where `<LUMP_HEX_ID>` is a four digit hexadecimal string

```
mp_rr_canyonlands.004a.bsp_lump -> 0x4A -> 74 -> VertexUnlitTS
```

Entities are stored across 5 different `.ent` files per `.bsp`.
The 5 files are: `env`, `fx`, `script`, `snd` & `spawn`

> Any string in `ENTITY_PARTITIONS` besides `*01` will work.

Titanfall 2 `.ent` files have a header similar to:
```
ENTITIES02 model_count=28
```

All `.ent` files will have the same `model_count` for each `.bsp`.

It's not entirely clear why respawn split up entities over multiple files.
Some possibilities:
 * optimised asset streaming
 * version control
   - e.g.  an artist can adjust `fx` while another dev handles `snd`
 * tracking entity budget by category
 * separation of concerns

We just don't know.



## Predecessors
### [Call of Duty 4: Modern Warfare](../infinity_ward/modern_warfare/index.md)
CoD 4 FastFiles (`*.ff`) also split up `.bsp`s
fastfiles were used for Infinity Ward's console CoDs before CoD4 brought them to PC


### [Quake 3](../id_software/quake3/index.md)
`.ent` files for entities has been traced back as far as Quake 3
Also home to QuakeC scripts used for level scripting

[Infinity Ward](../infinity_ward/index.md) would go on to use scripting extensively

Some Quake 3 variants began using "triangle soups"
An approach which plays well with GPUs & allows for more complex `.bsp` geo

Respawn's Source Engine fork goes hard on this approach
Seriously upgrading the engine's ability to render complex scenes


### Source Engine
Respawn uses a **heavily modified** version of [Valve](../valve/index.md)'s VScript
Specifically Squirrel[^sqre] `.nut` scripts

Most likely forked from either Left 4 Dead or Left 4 Dead 2's branch
Titanfall's engine was forked around 2011
Interestingly, Infra licensed Source from Valve around the same time

> TODO: citations needed



## Trivia
All Respawn's games give the error "Not an IBSP file" when `FILE_MAGIC` is incorrect
`IBSP` first appeared in [QuakeII](../id_software/quake2/index.md), a game which released in 1997.

Does this mean Apex Legends contains code from the Quake engine?
Yeah, probably.
But it's most likely **heavily modified**


## Further Reading
### GDC
<!-- Extreme SIMD -->
```embed
url: https://www.youtube.com/watch?v=6BIfqfC1i7U
```
<!-- Action Blocks -->
```embed
url: https://www.youtube.com/watch?v=CkHGuHd9BgU
```
<!-- Texture Streaming -->
```embed
url: https://www.youtube.com/watch?v=4BuvKotqpWo
```

### Steve Lee
<!-- Why Making Titanfall was Hard -->
```
url: https://www.youtube.com/watch?v=ZT9yVUDDUJg
```


[^sqre]: Northstar Modding Docs: [`squirrel_re`](https://docs.northstar.tf/Modding/squirrel/)
