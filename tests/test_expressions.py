# import maplibre.expressions
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
    e = expr.interpolate(column, stops, colors)
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
    e = expr.color_match_expr(column, categories)
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


def test_color_quantile_expr():
    # Prepare
    values = [1, 4, 2, 8, 9, 2, 3, 4]
    column = "test"
    probs = [0.25, 0.75]

    # Act
    e = expr.color_quantile_step_expr(column, probs=probs, values=values)
    print(e)

    # Assert
    assert e == [
        "step",
        ["get", "test"],
        "#440154",
        2.0,
        "#21908c",
        5.0,
        "#fde725",
    ]


def test_filter_expression():
    # Prepare
    column = "test"
    operator = ">="
    value = 0.5

    # Act
    e = expr.filter_expr(column, operator, value)
    print(e)

    # Assert
    assert e == [">=", ["get", "test"], 0.5]


def test_range_filter():
    # Prepare
    column = "test"
    operators = (">", "<")
    values = (0.5, 0.7)

    # Act
    e = expr.range_filter(column, values, operators)
    print(e)

    # Assert
    assert e == [
        "all",
        [">", ["get", "test"], 0.5],
        ["<", ["get", "test"], 0.7],
    ]
