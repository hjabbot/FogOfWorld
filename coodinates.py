class Position:
    """
    Stores coordinates with lat/lon labels
    """
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f'({self.lon},{self.lat})'