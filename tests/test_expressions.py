import maplibre.expressions as expr


def test_match_expression():
    # Prepare
    column = "letter"
    categories = ["A", "B", "C"]
    values = ["green", "blue", "red"]
    default_value = "yellow"

    # Act
    e = expr.match_expr(column, categories, values, default_value)
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
