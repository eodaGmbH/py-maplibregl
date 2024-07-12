from maplibre.color_utils import (
    create_categorical_color_expression,
    create_numeric_color_expression_from_breaks,
)


def test_create_categorical_color_expression():
    # Prepare
    values = ["A", "B"]
    column_name = "letter"
    cmap = "viridis"

    # Act
    cat_expression = create_categorical_color_expression(values, column_name, cmap)
    print(cat_expression)

    # Assert
    assert cat_expression == [
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


def test_numeric_color_expression_from_breaks():
    # Prepare
    column_name = "test"
    breaks = [2, 6]

    # Act
    expression = create_numeric_color_expression_from_breaks(column_name, breaks)
    print(expression)

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
