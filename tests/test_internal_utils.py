from os.path import splitext

from maplibre._utils import get_temp_filename


def test_get_temp_filename():
    filename = get_temp_filename()

    print(filename)
    filename, file_extension = splitext(filename)
    print(filename, file_extension)

    assert file_extension == ".html"
    assert "py-maplibre-gl-" in filename
