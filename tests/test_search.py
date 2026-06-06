from neuro_link import CommandEngine, NeuroInterface

def test_google_search_url(monkeypatch):
    ui = NeuroInterface()
    engine = CommandEngine(ui)

    opened = []

    def fake_open(url, *args):
        opened.append(url)

    engine.open_chrome = fake_open

    engine.handle_search("airbus a350")

    assert "google.com/search" in opened[0]
    assert "airbus" in opened[0]
