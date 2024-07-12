from maplibre.color_utils import create_categorical_color_expression


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
        "#414386",
        "B",
        "#fde725",
        "#000000",
    ]
