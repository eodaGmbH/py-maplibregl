from pymaplibregl.controls import Popup, PopupOptions


def test_popup():
    text = "some-text"

    popup = Popup(text=text)
    print(popup.to_dict())

    assert popup.to_dict()["text"] == "some-text"


def test_popup_options():
    # Prepare
    text = "some text"
    popup_options = PopupOptions(close_button=True)
    popup = Popup(text=text, options=popup_options)

    print(popup.to_dict())
    print(dict(popup))

    assert popup.to_dict()["text"] == text
    assert popup.to_dict()["options"] == {"closeButton": True}
