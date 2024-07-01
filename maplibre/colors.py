from PIL import ImageColor


def color_to_rgb(color):
    return ImageColor.getrgb(color)


def rgb_to_hex(rgb: tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def color_palette_rgb(
    rgb_source: tuple,
    rgb_target: tuple,
    n: int,
    max_value: int = 255,
) -> list[tuple]:
    n = n - 1
    steps = tuple(map(lambda i, j: (i - j) / n, rgb_target, rgb_source))
    r, g, b = rgb_source
    step_r, step_g, step_b = steps
    result = [
        (r + (i * step_r), g + (i * step_g), b + (i * step_b)) for i in range(n)
    ] + [rgb_target]
    if max_value == 255:
        return [tuple([round(item) for item in rgb]) for rgb in result]

    return result


def color_palette(color_source: str, color_target: str, n: int) -> list[str]:
    return [
        rgb_to_hex(color)
        for color in color_palette_rgb(
            color_to_rgb(color_source), color_to_rgb(color_target), n
        )
    ]
