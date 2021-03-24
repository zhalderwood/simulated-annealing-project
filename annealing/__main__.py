import random
import numpy
import math


class AssignmentState:
    def __init__(self, rooms):
        self.rooms = rooms
        self.fitness_high = 0
        self.fitness_low = 600
        self.fitness_avg = 0
        self.attempted_swaps = 0
        self.actual_swaps = 0

    @classmethod
    def initial(cls):
        rooms = [0] * 200  # create empty array for room assignments
        for i in range(200):
            rooms[i] = i
        random.shuffle(rooms)  # randomize order
        return AssignmentState(rooms)

    def get_rooms(self):
        return self.rooms

    def measure_fitness(self):
        total_score = 0
        print(self.rooms)
        for a, b, c, d in zip(*[iter(self.rooms)]*4):
            room_score = int(fitness[a][b])
            room_score += int(fitness[a][c])
            room_score += int(fitness[a][d])
            room_score += int(fitness[b][c])
            room_score += int(fitness[b][d])
            room_score += int(fitness[c][d])
            total_score += room_score
            if room_score < self.fitness_low:
                self.fitness_low = room_score
            if room_score > self.fitness_high:
                self.fitness_high = room_score
        self.fitness_avg = total_score / 50

    def __str__(self):
        template = "Average room fitness: {}\n" \
                   "Worst room fitness  : {}\n" \
                   "Best room fitness   : {}"
        return template.format(self.fitness_avg, self.fitness_high, self.fitness_low)

    def generate_swap(self):
        print("todo")

    def do_the_swap(self):
        print("todo")


fitness = [None] * 200


def get_fitness():  # open file of match ratings and add to array
    try:
        fitness_data = open('roommates.txt')
    except FileNotFoundError:
        print("Can't find file, exiting")
        return 1

    index = 0
    for rating in fitness_data:
        fitness[index] = rating.split()
        index += 1


def main():
    get_fitness()
    alpha_state = AssignmentState.initial()
    alpha_state.measure_fitness()
    print(alpha_state)


if __name__ == '__main__':
    main()
