from pymaplibregl.controls import ControlType, ScaleControl


def test_scale_control():
    control = ScaleControl()
    print(control.to_dict())

    assert control._name == ControlType.SCALE.value
    assert control.unit == "metric"


# def test_scale_control():
