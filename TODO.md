# TODO list

## load tables from .csv
this is a feature of the Material theme
could be a handy way of decoupling the db output from general prose (`.md` files)


## embedding cards
[Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten)

### Snippets extention?
Material for MkDocs > References > Tooltips > [Adding a glossary](https://squidfunk.github.io/mkdocs-material/reference/tooltips/?h=hover#adding-a-glossary)
[pymdownx.snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/)

> NOTE: PyMdown extensions comes with Properdocs

### useful cards to have
 * timeline snippets
   - engine forks & branches
   - game releases


## Lump System Entity Relationship Diagrams
Material for MkDocs > References > Diagrams > [Using entity-relationship diagrams](https://squidfunk.github.io/mkdocs-material/reference/diagrams/#using-entity-relationship-diagrams)
utilises mermaid


## Change favicon
Material for MkDocs > Setup > [Changing the logo and icons](https://squidfunk.github.io/mkdocs-material/setup/changing-the-logo-and-icons/?h=favicon#favicon)


## Python docs generator
### check coverage
ensure pages are present for every:
 - [ ] BspClass
 - [ ] ArchiveClass
 - [ ] DiscClass
 - [ ] BranchScript

### make snippets
generate `.csv` tables from `db` for:
 - [ ] Game lists
 - [ ] Branch relationship diagrams
 - [ ] LumpClass coverage
 - [ ] per-branch Toolsets
 * and a bunch of others I'm forgetting


### LumpClasses
 * use git-blame & python inspect to check code is current
   - put a note if updated since last release (stable vs. nightly)
   - automated warnings for if docs are outdated
 * tabbed C++ & Python code samples
   - revisit `.as_cpp`, design it for docs
   - common sub-structs based on `_classes` (e.g. Vector3)
 * link to definition on GitHub
 * indexing
   - lumps indexed
   - lumps indexed by
   - system(s) containing this lump


## Systems Pages
 - [ ] Relocate `branches.respawn.titanfall` system pages to `engines.resource.systems`
 - [ ] Include Engine links in each branch page
 - [ ] branches folder can be entirely generated docs
   - [ ] game lists
   - [ ] lump classes


## Miscellaneous
 - [ ] Fixup broken auto-capitalisation (lookup table?)
   - [ ] `Id software` -> `Id Software`
   - [ ] `Resource` -> `ReSource`
 - [ ] Other docs / wikis
   - [ ] `breki` will handle ArchiveClasses in future
   - [ ] `bite` will handle texture & material formats
   - [ ] `ass` will handle models (including bsp export)
 - [ ] GitHub discussions archive
   - [ ] good writing reference
   - [ ] cite external sources (Twitter, VDC, GDC etc.)
   - [ ] screenshots & video
