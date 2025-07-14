# `scenes.SceneDescription`

Base class of all [SceneClasses](../glossary/scene_classes.md)


## `ModelList`
```python
ModelList = Union[
    List[geometry.Model],  # list of models
    Dict[str, geometry.Model]]  # named models
```


## Methods
### Initialisers
`#!py def from_file(cls, filename: str) -> SceneDescription:`
:   open SceneDescription from a file

`#!py def from_models(cls, models: ModelList) -> SceneDescription:`
:   open SceneDescription from a ModelList


### Saving
`#!py def save_as(self, filename: str):`
:   save SceneDescription to a file
