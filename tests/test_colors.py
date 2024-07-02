from maplibre.colors import ColorPalette


def test_color_palette():
    codes = [1, 2, 3, 1, 2, 3]
    print(codes)
    pal = ColorPalette("red", "blue")

    colors = pal.get_colors(codes)
    print(colors)

    assert len(set(colors)) == 3


def test_color_palette_numeric():
    values = [1, 2, 3, 1, 2, 3]
    pal = ColorPalette("red", "blue")
    print(values)

    x = pal.numeric(values, 10)
    print(x)


def test_color_palette_factor():
    values = ["A", "B", "A", "C", "E"]
    pal = ColorPalette("red", "blue")
    print(values)

    x = pal.factor(values)
    print(x)
