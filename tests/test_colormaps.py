import maplibre.mplt_colormaps as colorutils


def test_colormaps():
    # Prepare
    cmap = "viridis"
    n = 10

    # Act
    colors = colorutils.create_colors(cmap, n)
    print(colors)

    # Assert
    assert len(colors) == 10
    assert colors[0] == "#440154"
    assert colors[-1] == "#fde725"


def test_numeric():
    x = [1, 2, 3, 1, 4, 3]
    bins = 2

    color_brewer = colorutils.ColorBrewer()
    colors, codes, _ = color_brewer.numeric(x, bins=bins)
    print(colors, codes)

    assert len(colors) == len(x)
    assert len(set(colors)) == 2
    assert len(set(codes)) == 2
    assert colors[0] == "#440154"
    assert colors[-1] == "#fde725"


def test_factor():
    x = [1, 2, 3, 1, 4, 3, 2]
    color_brewer = colorutils.ColorBrewer()
    colors, codes, _ = color_brewer.factor(x)
    print(colors, codes)

    assert len(colors) == len(x)
    expected = [0, 1, 2, 0, 3, 2, 1]
    assert all([a == b for a, b in zip(codes, expected)])
