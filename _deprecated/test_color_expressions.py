from _deprecated.color_utils import (
    create_categorical_color_expression,
    create_numeric_color_expression,
    create_numeric_color_expression_from_breaks,
    create_numeric_color_expression_from_quantiles,
)


def test_create_categorical_color_expression():
    # Prepare
    values = ["A", "B"]
    column_name = "letter"
    cmap = "viridis"

    # Act
    expression, unique_values, colors = create_categorical_color_expression(
        values, column_name, cmap
    )
    print(expression, unique_values, colors)

    # Assert
    assert expression == [
        "match",
        ["get", "letter"],
        "A",
        "#440154",
        "B",
        "#fde725",
        "#000000",
    ]


def test_create_numeric_color_expression():
    # Prepare
    values = [1, 4, 2, 8, 9]
    n = 3
    column_name = "test"

    # Act
    expression, breaks, colors = create_numeric_color_expression(values, n, column_name)
    print(expression, breaks, colors)

    # Assert
    colors = ["#440154", "#31678d", "#35b678", "#fde725"]


def test_numeric_color_expression_from_breaks():
    # Prepare
    column_name = "test"
    breaks = [2, 6]

    # Act
    expression, breaks, colors = create_numeric_color_expression_from_breaks(
        column_name, breaks
    )
    print(expression, breaks, colors)

    # Assert
    assert expression == [
        "step",
        ["get", "test"],
        "#440154",
        2,
        "#21908c",
        6,
        "#fde725",
    ]


def test_numeric_color_expression_from_quantiles():
    # Prepare
    values = [1, 4, 2, 8, 9, 2, 3, 4]
    column_name = "test"
    quantiles = [0.25, 0.75]

    # Act
    expression, breaks, colors = create_numeric_color_expression_from_quantiles(
        values, q=quantiles, column_name=column_name
    )
    print(expression, breaks, colors)

    # Assert
    assert expression == [
        "step",
        ["get", "test"],
        "#440154",
        2.0,
        "#21908c",
        5.0,
        "#fde725",
    ]
