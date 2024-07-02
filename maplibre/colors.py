from PIL import ImageColor


def color_to_rgb(color):
    return ImageColor.getrgb(color)


def rgb_to_hex(rgb: tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def color_palette_rgb(
    source_rgb: tuple,
    target_rgb: tuple,
    n: int,
    max_value: int = 255,
) -> list[tuple]:
    n = n - 1
    steps = tuple(map(lambda i, j: (i - j) / n, target_rgb, source_rgb))
    r, g, b = source_rgb
    step_r, step_g, step_b = steps
    result = [
        (r + (i * step_r), g + (i * step_g), b + (i * step_b)) for i in range(n)
    ] + [target_rgb]
    if max_value == 255:
        return [tuple([round(item) for item in rgb]) for rgb in result]

    return result


def color_palette(source_color: str, target_color: str, n: int) -> list[str]:
    return [
        rgb_to_hex(color)
        for color in color_palette_rgb(
            color_to_rgb(source_color), color_to_rgb(target_color), n
        )
    ]
