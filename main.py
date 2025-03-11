from locations import Terminator, Country, City
from trips import Trip
from maps import TerminatorMap, CityMap, TripMap, CountryMap, CombinedMap

if __name__ == '__main__':
    current_terminator = Terminator()
    terminator_map = TerminatorMap(current_terminator)