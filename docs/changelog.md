# Changelog for MapLibre for Python

## maplibre v0.2.3 (unreleased)

* Add interactive attributes to IpyWidget
  * `Map.center`
  * `Map.bounds`
  * `Map.zoom`
  * `Map.lat_lng` > `Map.clicked` (rename)
* Change map option types
  * MapOptions.zoom: int > float
  * MapOptions.bearing: int > float
  * MapOptions.pitch: int > float

## maplibre v0.2.2

* Add support for PMTiles (#55)

## maplibre v0.2.1

* Do not add navigation control by default (#31)

## maplibre v0.2.0

* Support Deck.GL layers (#28)

## maplibre v0.1.6

* Add `before_id` parameter to `add_layer` method (#45, #47)
* Add example showing how to insert a layer before labels

## maplibre v0.1.5

* Update deprecated render function to support `shiny>=0.7.0`

## maplibre v0.1.4

* `anywidget>=0.9.0` (#36)

## maplibre v0.1.3

* Display all properties in popup and tooltip if `prop = None` (#26)
* Support [mustache](https://github.com/janl/mustache.js) templates for popups and tooltips (#27)

## maplibre v0.1.2

* Add `Map.set_data`
* Add `Map.set_visibility`
* Do not import `ipywidget.MapWidget` in `__init__` and skip tests for `MapWidget`, because it causes a `core dumped` error, see [anywidget issue](https://github.com/manzt/anywidget/issues/374)
* Remove `requests` dependency
* Remove dead code
* Add more examples

## maplibre v0.1.1

* Initial PyPI release
