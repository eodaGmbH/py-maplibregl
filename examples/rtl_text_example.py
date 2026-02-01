"""
Visual test for RTL (Right-to-Left) text plugin.

This script creates a map centered on Zamalek, Cairo with Arabic labels
to verify that RTL text rendering works correctly.

Run with: uv run python examples/rtl_text_example.py
"""

from maplibre import Map, MapOptions

# Create a map centered on Zamalek, Cairo - to test Arabic RTL text
m = Map(
    MapOptions(
        # Use a style with multilingual labels (OpenStreetMap-based)
        style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
        center=(31.2243, 30.0626),  # Zamalek, Cairo, Egypt
        zoom=14,
    )
)

# Save and open in browser
filename = m.save(filename="rtl_test_map.html", title="RTL Text Test - Zamalek, Cairo")
print(f"Map saved to: {filename}")
print("Check that Arabic text renders correctly (right-to-left)")
