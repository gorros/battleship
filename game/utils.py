import re


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    @staticmethod
    def str_to_coordinate(s):
        coordinate = list(map(int, re.findall(r'\d+', s)))
        if len(coordinate) != 2:
            raise ValueError("Wrong coordinate format")
        return Coordinate(coordinate[0], coordinate[1])
