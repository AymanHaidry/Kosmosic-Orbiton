def test_youtube_search(monkeypatch):
    opened = []

    engine.open_chrome = lambda url, *args: opened.append(url)

    engine.handle_youtube("python tutorial")

    assert "youtube.com/results" in opened[0]
