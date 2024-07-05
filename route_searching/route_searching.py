import math
import random
from random import randint
from math import *
import os
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"
from matplotlib import pyplot as plt


class City:
    def __init__(self, cords: tuple[int, int]):
        self.cords = cords
        self.roads = {}


class Road:
    def __init__(self, city1, city2):
        self.distance = sqrt((city1.cords[0] - city2.cords[0])**2 + (city1.cords[1] - city2.cords[1])**2)


class Infrastructure:
    def __init__(self, number_of_cities: int, cords_range: tuple[int, int]) -> None:
        self.city_of_origin = None
        self.cities_cords = set()
        self.cities = set()
        self.number_of_roads = 0
        while (len(self.cities_cords) != number_of_cities and len(self.cities_cords) !=
               (cords_range[1] - cords_range[0] + 1)**2):
            self.cities_cords.add((randint(cords_range[0], cords_range[1]), randint(cords_range[0], cords_range[1])))
        for cords in self.cities_cords:
            self.cities.add(City(cords))
        for city in self.cities:
            self.city_of_origin = city
            break
        for city1 in self.cities:
            for city2 in self.cities:
                if city2 is not city1:
                    city1.roads[city2] = (Road(city1, city2))
                    if city1 not in city2.roads.keys():
                        self.number_of_roads += 1

    def ensure_2_roads(self, cities_with_2_roads: set[City]) -> bool:
        for cityA in (self.cities - cities_with_2_roads):
            for cityB in cityA.roads.keys():
                if len(cityB.roads) > 2:
                    break
            else:
                continue
            break
        else:
            return False
        return True

    def leave_percentage_of_roads(self, percentage: float) -> None:
        destroyed_num = round((100 - percentage) / 100 * self.number_of_roads)
        already_destroyed = 0
        cities_with_2_roads = set()
        while self.number_of_roads > len(self.cities) and already_destroyed != destroyed_num:
            city1 = random.choice(tuple(self.cities))
            city2 = random.choice(tuple(city1.roads.keys()))
            while len(city1.roads) <= 2 or len(city2.roads) <= 2:
                if len(city1.roads) <= 2:
                    cities_with_2_roads.add(city1)
                else:
                    cities_with_2_roads.add(city2)
                city1 = random.choice(tuple(self.cities - cities_with_2_roads))
                city2 = random.choice(tuple(city1.roads.keys()))
                if not self.ensure_2_roads(cities_with_2_roads):
                    return
            city1.roads.pop(city2)
            city2.roads.pop(city1)
            self.number_of_roads -= 1
            already_destroyed += 1

    def show_infrastructure(self) -> None:
        plt.xlim(-100, 100)
        plt.ylim(-100, 100)
        plt.grid()
        x_cords = [cord[0] for cord in self.cities_cords]
        y_cords = [cord[1] for cord in self.cities_cords]
        plt.plot(x_cords, y_cords, 'o', color="blue")
        for city1 in self.cities:
            for city2 in city1.roads.keys():
                plt.plot([city1.cords[0], city2.cords[0]], [city1.cords[1], city2.cords[1]], color="blue")
        plt.show()

    def add_new_path(self, path: str, city: City, new_visited_cities: list[City],
                     distance: float) -> tuple[str, list, float]:
        new_path = path + str(city.cords)
        new_visited_cities.append(city)
        new_distance = distance + new_visited_cities[-2].roads[city].distance
        if (len(new_visited_cities) == len(self.cities) and
                new_visited_cities.index(self.city_of_origin) == 0):
            new_visited_cities.pop(0)
        return new_path, new_visited_cities, new_distance

    def show_shortest_path_for_bfs(self, paths: dict[str: tuple[list[City]], float]) -> None:
        distances = {}
        for items in paths.items():
            if round(items[1][1] * 1000) / 1000 in distances.keys():
                distances[round(items[1][1] * 1000) / 1000].append((items[0], items[1][0]))
            else:
                distances[round(items[1][1] * 1000) / 1000] = [(items[0], items[1][0])]
        if len(distances[min(distances.keys())][0][1]) == len(self.cities):
            print(f"BFS\ndistance: {min(distances.keys())}\npath: {distances[min(distances.keys())][0][0]}\n")
        else:
            print("impossible path")

    def breadth_first_search(self) -> None:
        paths = {str(self.city_of_origin.cords): ([self.city_of_origin], 0)}
        new_paths = {}
        while True:
            changes = 0
            for path in paths.keys():
                visited_cities, distance = paths[path][0], paths[path][1]
                for city in visited_cities[-1].roads.keys():
                    if city not in visited_cities:
                        new_path, new_visited_cities, new_distance = (
                            self.add_new_path(path, city, visited_cities.copy(), distance))
                        new_paths[new_path] = (new_visited_cities, new_distance)
                        changes += 1
            if not changes:
                break
            paths = new_paths.copy()
            new_paths = {}
        self.show_shortest_path_for_bfs(paths)

    def dfs_execution(self, current_city: City, visited_cities: list[City], path: float) -> tuple[float, list]:
        min_path = []
        min_distance = math.inf
        if len(visited_cities) == len(self.cities):
            if current_city in self.city_of_origin.roads:
                new_path = visited_cities
                new_path.append(self.city_of_origin)
                return path + self.city_of_origin.roads[current_city].distance, new_path
        for city in current_city.roads:
            if city in visited_cities:
                continue
            new_visited_cities = visited_cities.copy()
            new_visited_cities.append(city)
            new_path = self.dfs_execution(city, new_visited_cities, path + current_city.roads[city].distance)
            if new_path[0] < min_distance:
                min_distance = new_path[0]
                min_path = new_path[1]
        return min_distance, min_path

    def depth_first_search(self) -> None:
        path = self.dfs_execution(self.city_of_origin, [self.city_of_origin], 0)
        name = str()
        for city in path[1]:
            name += str(city.cords)
        if path[0] != math.inf:
            print(f"DFS\ndistance: {round(path[0] * 1000) / 1000}\npath: {name}\n")
        else:
            print("DFS\nimpossible path\n")

    @staticmethod
    def pick_shortest_paths(visited_cities: list[City], path_len_lim: float,
                            roads_list: list[tuple[City, City]]) -> int:
        changes = 0
        for city in visited_cities:
            for road in city.roads:
                if road not in visited_cities and city.roads[road].distance <= path_len_lim:
                    roads_list.append((city, road))
                    visited_cities.append(road)
                    changes += 1
        return changes

    @staticmethod
    def set_new_path_len(visited_cities: list[City], path_len_lim: float) -> float:
        new_path_len_lim = math.inf
        for city in visited_cities:
            for road in city.roads:
                if new_path_len_lim > city.roads[road].distance > path_len_lim:
                    new_path_len_lim = city.roads[road].distance
        return new_path_len_lim

    def build_mst(self) -> list[tuple[City, City]]:
        visited_cities = [self.city_of_origin]
        path_len_lim = 0
        roads_list = []
        while len(roads_list) < len(self.cities) - 1:
            changes = self.pick_shortest_paths(visited_cities, path_len_lim, roads_list)
            if not changes:
                path_len_lim = self.set_new_path_len(visited_cities, path_len_lim)
        return roads_list

    def find_path(self, visited_cities: list[City]) -> None:
        current_city = self.city_of_origin
        mst = self.build_mst()
        first_leaf_achieved = 0
        while len(visited_cities) < len(self.cities):
            for road in mst:
                if road[0] == current_city and road[1] not in visited_cities:
                    current_city = road[1]
                    if first_leaf_achieved == 0:
                        visited_cities.append(road[1])
                    break
            else:
                if first_leaf_achieved > 0 and current_city not in visited_cities:
                    visited_cities.append(current_city)
                first_leaf_achieved += 1
                current_city = visited_cities[visited_cities.index(current_city) - 1]

    def execute_mst(self) -> None:
        visited_cities = [self.city_of_origin]
        self.find_path(visited_cities)
        visited_cities.append(self.city_of_origin)
        path = str()
        distance = 0
        for count, city in enumerate(visited_cities):
            if count != len(visited_cities) - 1:
                distance += city.roads[visited_cities[visited_cities.index(city) + 1]].distance
            path += str(city.cords)
        print(f"MST\ndistance: {round(distance * 1000) / 1000}\npath: {path}\n")

    @staticmethod
    def choose_next_city(current_city: City, visited_cities: list[City], last_city: City or None) -> City:
        min_path = math.inf
        next_city = None
        for city in current_city.roads:
            if (current_city.roads[city].distance < min_path and
                    city not in visited_cities and not last_city):
                min_path = current_city.roads[city].distance
                next_city = city
        return next_city

    def check_path(self, visited_cities: list[City], last_city: City) -> tuple[City or None, City or None]:
        returned_cities = set()
        for city in reversed(visited_cities):
            returned_cities.add(city)
            last_city = city
            if (len(visited_cities) == len(self.cities) and self.city_of_origin in city.roads and not
               set(visited_cities[visited_cities.index(city) - 1].roads.keys()).isdisjoint(returned_cities)):
                break
        if last_city == visited_cities[-1]:
            return None, None
        else:
            index = visited_cities.index(last_city)
            for i in range(len(self.cities) - index):
                visited_cities.pop(index)
            return visited_cities[-1], last_city

    @staticmethod
    def show_shortest_path_for_gs(visited_cities: list[City]) -> None:
        path = str()
        distance = 0
        for count, city in enumerate(visited_cities):
            if count != len(visited_cities) - 1:
                distance += city.roads[visited_cities[visited_cities.index(city) + 1]].distance
            path += str(city.cords)
        print(f"GREEDY\ndistance: {round(distance * 1000) / 1000}\npath: {path}\n")

    def greedy_search(self) -> None:
        current_city = self.city_of_origin
        visited_cities = [self.city_of_origin]
        last_city = None
        while True:
            current_city = self.choose_next_city(current_city, visited_cities, last_city)
            if current_city is None:
                print("GREEDY\nimpossible path\n")
                return
            visited_cities.append(current_city)
            if len(visited_cities) == len(self.cities) or set(visited_cities[-1].roads.keys()) > set(visited_cities):
                current_city, last_city = self.check_path(visited_cities, last_city)
                if current_city is None and last_city is None:
                    break
        visited_cities.append(self.city_of_origin)
        self.show_shortest_path_for_gs(visited_cities)

    @staticmethod
    def break_loop(start_paths: dict[str: tuple[list[City], City]],
                   end_paths: dict[str: tuple[list[City], City]]) -> bool:
        for start_path in start_paths:
            for end_path in end_paths:
                if start_paths[start_path][1] == end_paths[end_path][1]:
                    return True
        return False

    @staticmethod
    def visit_next_cities(paths: dict[str: tuple[list[City], City]]) -> None:
        for path in paths.copy():
            for city in paths[path][1].roads:
                if city not in paths[path][0]:
                    paths[path + str(city.cords)] = (paths[path][0] + [city], city)
            paths.pop(path)

    def find_parted_paths(self, start_paths: dict[str: tuple[list[City], City]],
                          end_paths: dict[str: tuple[list[City], City]]) -> None:
        while True:
            self.visit_next_cities(start_paths)
            if self.break_loop(start_paths, end_paths):
                break
            self.visit_next_cities(end_paths)
            if self.break_loop(start_paths, end_paths):
                break

    @staticmethod
    def create_whole_paths(start_paths: dict[str: tuple[list[City], City]],
                           end_paths: dict[str: tuple[list[City], City]]) -> list[list[City]]:
        paths = []
        parted_paths = []
        for start_path in start_paths:
            for end_path in end_paths:
                if start_paths[start_path][1] == end_paths[end_path][1]:
                    parted_paths.append((start_paths[start_path][0], end_paths[end_path][0]))
        for parted_path in parted_paths:
            path = []
            for city in parted_path[0]:
                path.append(city)
            for count, city in enumerate(reversed(parted_path[1])):
                if count:
                    path.append(city)
            paths.append(path)
        return paths

    @staticmethod
    def show_shortest_path_for_bds(paths: list[list[City]]) -> None:
        distances = {}
        for path in paths:
            distance = 0
            name = str()
            for count, city in enumerate(path):
                if count < len(path) - 1:
                    distance += city.roads[path[count + 1]].distance
                name += str(city.cords)
            distances[name] = distance
        print(f"BDS\ndistance: {distances[min(distances, key=distances.get)]}\n"
              f"path: {min(distances, key=distances.get)}")

    def bidirectional_search(self) -> None:
        start_city = self.city_of_origin
        end_city = self.city_of_origin
        while len(start_city.roads) == len(self.cities) - 1:
            start_city = random.choice(tuple(self.cities))
        while start_city == end_city or start_city in end_city.roads:
            end_city = random.choice(tuple(self.cities - set(start_city.roads.keys())))
        start_paths = {str(start_city.cords): ([start_city], start_city)}
        end_paths = {str(end_city.cords): ([end_city], end_city)}
        self.find_parted_paths(start_paths, end_paths)
        paths = self.create_whole_paths(start_paths, end_paths)
        self.show_shortest_path_for_bds(paths)


if __name__ == "__main__":
    infrastructure = Infrastructure(5, (-100, 100))
    percentage_of_roads = 100
    infrastructure.leave_percentage_of_roads(percentage_of_roads)
    infrastructure.breadth_first_search()
    infrastructure.depth_first_search()
    if percentage_of_roads == 100:
        infrastructure.greedy_search()
        infrastructure.execute_mst()
    if percentage_of_roads < 100:
        infrastructure.bidirectional_search()
    infrastructure.show_infrastructure()
