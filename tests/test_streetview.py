def test_streetview_opens(monkeypatch):
    opened = []

    engine.open_chrome = lambda url, *args: opened.append(url)

    engine.handle_streetview()

    assert "google.com/maps" in opened[0]
