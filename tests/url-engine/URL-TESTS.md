This should give you 9 URL-engine tests immediately:

✓ Google Search
✓ YouTube Search
✓ Weather (city)
✓ Weather (default)
✓ Airport Search
✓ Flight Tracking
✓ METAR
✓ Maps
✓ Street View

One thing I'd improve in Neuro-Link first: extract URL generation into dedicated methods like:

build_search_url()
build_youtube_url()
build_track_url()
build_maps_url()

Then tests become pure:

assert engine.build_track_url("EK568") \
    == "https://www.flightradar24.com/EK568"

Those are faster, cleaner, and don't need monkeypatching at all. That's how larger projects usually evolve once the feature set stabilizes.
