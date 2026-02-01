"""
RTL Text Plugin Test - Marimo

Run with: marimo run examples/rtl_test_marimo.py
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    from maplibre import MapOptions
    from maplibre.ipywidget import MapWidget as Map

    # Create a map centered on Zamalek, Cairo - to test Arabic RTL text
    m = Map(
        MapOptions(
            style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
            center=(31.2243, 30.0626),  # Zamalek, Cairo, Egypt
            zoom=14,
        ),
        height=600,
    )

    mo.md("""
    # RTL Text Plugin Test - Marimo

    Arabic street names and place labels should render correctly:
    - Text flows right-to-left
    - Characters are connected properly
    """)
    return m, mo


@app.cell
def _(m):
    m
    return


if __name__ == "__main__":
    app.run()
