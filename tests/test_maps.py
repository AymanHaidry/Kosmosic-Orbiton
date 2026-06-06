def test_maps_search():
    ...
    engine.handle_maps("times square")

    assert "google.com/maps" in opened[0]
