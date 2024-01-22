# Changelog for MapLibre for Python

## maplibre v0.1.2

* Add `Map.set_data`
* Add `Map.set_visibility`
* Do not import `ipywidget.MapWidget` in `__init__` and skip tests for `MapWidget`, because it causes a `core dumped` error, see [anywidget issue](https://github.com/manzt/anywidget/issues/374)
* Remove `requests` dependency
* Remove dead code
* Add more examples

## maplibre v0.1.1

* Initial PyPI release