from maplibre.controls import ControlType, ScaleControl


def test_scale_control():
    control = ScaleControl()
    print(control.to_dict())

    assert control.type == ControlType.SCALE.value
    assert control.unit == "metric"
