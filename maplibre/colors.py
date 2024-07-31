from __future__ import annotations

try:
    from branca.utilities import color_brewer as branca_color_brewer
except ImportError as e:
    print(e)
    branca_color_brewer = None

CMAPS_JSON = "https://raw.githubusercontent.com/python-visualization/branca/main/branca/_schemes.json"
# FALLBACK_COLOR = "#000000"
DEFAULT_CMAP = "viridis"


def color_brewer(cmap: str, n: int) -> list:
    n = int(n)
    if n == 2:
        colors = branca_color_brewer(cmap)
        return [colors[i] for i in [0, -1]]

    return branca_color_brewer(cmap, n)


def list_cmaps() -> list | None:
    try:
        import requests
    except ImportError as e:
        print(e)
        return

    return list(requests.get(CMAPS_JSON).json().keys())


# Taken from https://github.com/karthik/wesanderson
wes_palettes = dict(
    BottleRocket1=(
        "#A42820",
        "#5F5647",
        "#9B110E",
        "#3F5151",
        "#4E2A1E",
        "#550307",
        "#0C1707",
    ),
    BottleRocket2=("#FAD510", "#CB2314", "#273046", "#354823", "#1E1E1E"),
    Rushmore1=("#E1BD6D", "#EABE94", "#0B775E", "#35274A", "#F2300F"),
    Rushmore=("#E1BD6D", "#EABE94", "#0B775E", "#35274A", "#F2300F"),
    Royal1=("#899DA4", "#C93312", "#FAEFD1", "#DC863B"),
    Royal2=("#9A8822", "#F5CDB4", "#F8AFA8", "#FDDDA0", "#74A089"),
    Zissou1=("#3B9AB2", "#78B7C5", "#EBCC2A", "#E1AF00", "#F21A00"),
    Zissou1Continuous=(
        "#3A9AB2",
        "#6FB2C1",
        "#91BAB6",
        "#A5C2A3",
        "#BDC881",
        "#DCCB4E",
        "#E3B710",
        "#E79805",
        "#EC7A05",
        "#EF5703",
        "#F11B00",
    ),
    Darjeeling1=("#FF0000", "#00A08A", "#F2AD00", "#F98400", "#5BBCD6"),
    Darjeeling2=("#ECCBAE", "#046C9A", "#D69C4E", "#ABDDDE", "#000000"),
    Chevalier1=("#446455", "#FDD262", "#D3DDDC", "#C7B19C"),
    FantasticFox1=("#DD8D29", "#E2D200", "#46ACC8", "#E58601", "#B40F20"),
    Moonrise1=("#F3DF6C", "#CEAB07", "#D5D5D3", "#24281A"),
    Moonrise2=("#798E87", "#C27D38", "#CCC591", "#29211F"),
    Moonrise3=("#85D4E3", "#F4B5BD", "#9C964A", "#CDC08C", "#FAD77B"),
    Cavalcanti1=("#D8B70A", "#02401B", "#A2A475", "#81A88D", "#972D15"),
    GrandBudapest1=("#F1BB7B", "#FD6467", "#5B1A18", "#D67236"),
    GrandBudapest2=("#E6A0C4", "#C6CDF7", "#D8A499", "#7294D4"),
    IsleofDogs1=("#9986A5", "#79402E", "#CCBA72", "#0F0D0E", "#D9D0D3", "#8D8680"),
    IsleofDogs2=("#EAD3BF", "#AA9486", "#B6854D", "#39312F", "#1C1718"),
    FrenchDispatch=("#90D4CC", "#BD3027", "#B0AFA2", "#7FC0C6", "#9D9C85"),
    AsteroidCity1=("#0A9F9D", "#CEB175", "#E54E21", "#6C8645", "#C18748"),
    AsteroidCity2=("#C52E19", "#AC9765", "#54D8B1", "#b67c3b", "#175149", "#AF4E24"),
    AsteroidCity3=("#FBA72A", "#D3D4D8", "#CB7A5C", "#5785C1"),
)
