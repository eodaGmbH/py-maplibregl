# the starting color
initial_color = (0.60156, 0, 0.99218)  # (154, 0, 254)

# the final, target color
target_color = (0.86328, 0.47656, 0.31250)  # (221, 122, 80)

number_of_rows = 10  # how many rows we're painting

# get the total difference between each color channel
red_difference = target_color[0] - initial_color[0]
green_difference = target_color[1] - initial_color[1]
blue_difference = target_color[2] - initial_color[2]

# divide the difference by the number of rows, so each color changes by this amount per row
red_delta = red_difference / number_of_rows
green_delta = green_difference / number_of_rows
blue_delta = blue_difference / number_of_rows

# display the color for each row
for i in range(0, number_of_rows):
    # apply the delta to the red, green and blue channels
    interpolated_color = (
        initial_color[0] + (red_delta * i),
        initial_color[1] + (green_delta * i),
        initial_color[2] + (blue_delta * i),
    )
    print(interpolated_color)


# res = tuple(ele1 * ele2 for ele1, ele2 in zip(test_tup1, test_tup2))
def color_palette(rgb_source: tuple, rgb_target: tuple, n: int) -> list:
    steps = tuple(map(lambda i, j: (i - j) / n, rgb_target, rgb_source))
    r, g, b = rgb_source
    step_r, step_g, step_b = steps
    result = [(r + (i * step_r), g + (i * step_g), b + (i * step_b)) for i in range(n)]
    return result + [target_color]


print(color_palette(initial_color, target_color, number_of_rows))
