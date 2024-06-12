import random
from random import randint
from math import *


class City:
    def __init__(self, cords: tuple[int, int]):
        self.cords = cords
        self.roads = {}


class Road:
    def __init__(self, city1, city2):
        self.distance = sqrt((city1.cords[0] - city2.cords[0])**2 + (city1.cords[1] - city2.cords[1])**2)


class Infrastructure:
    def __init__(self, number_of_cities: int, cords_range: tuple[int, int]) -> None:
        self.cities_cords = set()
        self.cities = set()
        self.number_of_roads = 0
        while (len(self.cities_cords) != number_of_cities and len(self.cities_cords) !=
               (cords_range[1] - cords_range[0] + 1)**2):
            self.cities_cords.add((randint(cords_range[0], cords_range[1]), randint(cords_range[0], cords_range[1])))
        for cords in self.cities_cords:
            self.cities.add(City(cords))
        for city1 in self.cities:
            for city2 in self.cities:
                if city2 is not city1:
                    city1.roads[city2] = (Road(city1, city2))
                    if city1 not in city2.roads.keys():
                        self.number_of_roads += 1

    def leave_percentage_of_roads(self, percentage: float) -> None:
        destroyed_num = round((100 - percentage) / 100 * self.number_of_roads)
        already_destroyed = 0
        while self.number_of_roads >= len(self.cities) and already_destroyed != destroyed_num:
            city1 = random.choice(tuple(self.cities))
            while len(city1.roads) < 2:
                city1 = random.choice(tuple(self.cities))
            city2 = random.choice(tuple(city1.roads.keys()))
            while len(city2.roads) < 2:
                city2 = random.choice(tuple(city1.roads.keys()))
            city1.roads.pop(city2)
            city2.roads.pop(city1)
            self.number_of_roads -= 1
            already_destroyed += 1

    def breadth_first_search(self):
        pass


if __name__ == "__main__":
    infrastructure = Infrastructure(5, (-100, 100))
    infrastructure.leave_percentage_of_roads(80)
    infrastructure.breadth_first_search()
