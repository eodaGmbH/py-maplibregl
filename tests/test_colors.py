from maplibre.colors import ColorPalette


def test_color_palette():
    codes = [1, 2, 3, 1, 2, 3]
    pal = ColorPalette("red", "blue")

    colors = pal.get_colors(codes, n=4)
    print(colors)

    assert len(set(colors)) == 3
