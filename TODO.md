## load tables from .csv
this is a feature of the Material theme
could be a handy way of decoupling the db output from general prose (`.md` files)


## embedding cards
[Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten)

### Snippets extention?
Material for MkDocs > References > Tooltips > [Adding a glossary](https://squidfunk.github.io/mkdocs-material/reference/tooltips/?h=hover#adding-a-glossary)
[pymdownx.snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/)

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
 * tabbed C++ & Python code samples
   - revisit `.as_cpp`, design it for docs
   - common sub-structs based on `_classes` (e.g. Vector3)
