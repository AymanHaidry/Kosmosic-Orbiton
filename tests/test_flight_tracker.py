def test_flight_tracking():
    ...
    engine.handle_track("EK568")

    assert "flightradar24.com" in opened[0]
