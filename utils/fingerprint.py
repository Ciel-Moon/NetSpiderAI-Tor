import random

def randomize_fingerprint():
    """Return a dict with random viewport and other browser properties."""
    widths = [1024, 1280, 1366, 1440, 1536, 1600, 1920]
    heights = [600, 720, 768, 800, 864, 900, 1080]
    return {
        'viewport': {'width': random.choice(widths), 'height': random.choice(heights)},
        'timezone': random.choice(['America/New_York', 'Europe/London', 'Asia/Tokyo']),
        'language': random.choice(['en-US', 'en-GB', 'ja-JP'])
    }
