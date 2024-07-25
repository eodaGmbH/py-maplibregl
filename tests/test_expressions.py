import maplibre.colors as color_expr
import maplibre.expressions as expr


def test_match_expression():
    # Prepare
    column = "letter"
    categories = ["A", "B", "C"]
    colors = ["green", "blue", "red"]
    fallback = "yellow"

    # Act
    e = expr.match_expr(column, categories, colors, fallback)
    print(e)

    # Assert
    expected_expr = [
        "match",
        ["get", column],
        "A",
        "green",
        "B",
        "blue",
        "C",
        "red",
        "yellow",
    ]
    assert e == expected_expr


def test_interpolate_linear():
    # Prepare
    column = "growth"
    stops = [0, 1.0]
    colors = ["yellow", "red"]

    # Act
    e = expr.interpolate_linear(column, stops, colors)
    print(e)

    # Assert
    assert isinstance(e, list)
    assert e == ["interpolate", ["linear"], ["get", "growth"], 0, "yellow", 1.0, "red"]


def test_step_expression():
    # Prepare
    column = "value"
    stops = [100, 200, 300]
    colors = ["yellow", "red", "green"]
    fallback = "black"

    # Act
    e = expr.step_expr(column, stops, colors, fallback)
    print(e)

    expected_expr = [
        "step",
        ["get", "value"],
        "yellow",
        100,
        "red",
        200,
        "green",
        300,
        "black",
    ]

    assert e == expected_expr
    assert isinstance(e, list)


def test_color_match_expression():
    # Prepare
    column = "cat"
    categories = ["A", "B", "C", "B", "A"]

    # Act
    e = color_expr.color_match_expr(column, categories)
    print(e)

    # Assert
    expected_expr = [
        "match",
        ["get", "cat"],
        "A",
        "#440154",
        "B",
        "#31678d",
        "C",
        "#35b678",
        "#fde725",
    ]
    assert e == expected_expr
