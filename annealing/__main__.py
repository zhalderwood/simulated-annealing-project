import random
import datetime
import time


class SimulateAnnealingTool:
    def __init__(self):
        self.rooms = []
        self.new_rooms = []
        self.fitness_avg = 0
        self.fitness_high = 0
        self.fitness_low = 600
        self.attempted_swaps = 0
        self.actual_swaps = 0
        self.seq_non_swaps = 0
        self.current_temp = initial_temp
        self.cooling = cooling

        self.fitness_table = get_fitness_table()
        self.__get_initial_rooms()
        temp = self.__get_fitness_all(self.rooms)
        self.fitness_avg = temp[0]
        self.fitness_high = temp[1]
        self.fitness_low = temp[2]

    def __get_initial_rooms(self):
        # creates random initial rooms state
        temp_rooms = []  # empty array for room assignments
        for i in range(200):
            temp_rooms.append(i)
        random.shuffle(temp_rooms)  # randomize order
        print(temp_rooms)
        divided_rooms = []
        for a, b, c, d in zip(*[iter(temp_rooms)] * 4):
            temp = [a, b, c, d, 0]
            divided_rooms.append(temp)  # subdivide, saving a spot for room score
        self.rooms = divided_rooms

    def __get_fitness_all(self, rooms):
        # returns avg, high, and low fitness for provided rooms state
        high = 0
        low = 600
        total = 0
        index = 0
        for room in rooms:
            room_score = 0
            room_score += int(self.fitness_table[room[0]][room[1]])
            room_score += int(self.fitness_table[room[0]][room[2]])
            room_score += int(self.fitness_table[room[0]][room[3]])
            room_score += int(self.fitness_table[room[1]][room[2]])
            room_score += int(self.fitness_table[room[1]][room[3]])
            room_score += int(self.fitness_table[room[2]][room[3]])
            rooms[index][4] = room_score  # save score for this room's state
            if room_score < low:
                low = room_score
            if room_score > high:
                high = room_score
            total += room_score  # aggregate scores to calculate avg
            index += 1
        return [total / len(rooms), high, low]

    def __sort_rooms(self):
        # sort rooms by student num, then sort room list
        for index in range(len(self.rooms)):
            score = self.rooms[index].pop(4)  # remove score and room number then re-append
            self.rooms[index].sort()
            self.rooms[index].append(score)
        self.rooms = sorted(self.rooms, key=lambda x: x[0])

    def __get_stats_template(self):
        # returns a formatted string of various info about the current state of the object
        temp_str = "Initial temperature: {}   Ending temperature: {}\n".format(initial_temp, self.current_temp)
        cool_str = "Cooling schedule: T = {}T after 2000 swaps or 20000 attempts\n".format(self.cooling)
        swap_str = "Attempted swaps: {:,}   Actual swaps: {:,}\n".format(self.attempted_swaps, self.actual_swaps)
        fit_str = """
            Average room fitness: {}
            Worst room fitness  : {}
            Best room fitness   : {}
            \n""".format(self.fitness_avg, self.fitness_high, self.fitness_low)
        return temp_str + cool_str + swap_str + fit_str

    def __get_rooms_template(self):
        # returns a formatted string of current room state
        rooms_str = "Each line below is a single room assignment\n"
        for room in self.rooms:
            rooms_str += "Students: {:>3}, {:>3}, {:>3}, {:>3};   Room Fitness: {:>3}\n".format(
                room[0], room[1], room[2], room[3], room[4])
        return rooms_str

    def __str__(self):
        # print function to provide nice output for debugging
        self.__sort_rooms()
        return self.__get_stats_template() + self.__get_rooms_template()

    def save_to_file(self):
        # writes stats and room state to file
        self.__sort_rooms()
        file_name = "results_{}.txt".format(datetime.datetime.now().strftime("%y%j%H%M%S"))
        output_file = open(file_name, 'w')
        output_file.writelines([self.__get_stats_template(), self.__get_rooms_template()])
        output_file.close()

    def __swap_double(self):
        # swap first 2 students in one random room with last 2 students in another room
        room_nums = []
        for i in range(50):
            room_nums.append(i)
        swap1 = room_nums.pop(random.randrange(50))
        swap2 = room_nums.pop(random.randrange(49))
        new_rooms = self.rooms
        temp_stu = [new_rooms[swap2][0], new_rooms[swap2][1]]
        new_rooms[swap2][0] = new_rooms[swap1][2]
        new_rooms[swap2][1] = new_rooms[swap1][3]
        new_rooms[swap1][2] = temp_stu[0]
        new_rooms[swap1][3] = temp_stu[1]
        return new_rooms

    def __swap_single(self):
        # swap one random student in a random room with one random student in another room
        stu_nums = []
        for i in range(200):
            stu_nums.append(i)
        rand_index = random.randrange(200)
        swap1 = stu_nums.pop(rand_index)
        room1 = swap1 // 4
        stu1 = swap1 % 4
        rand_index = random.randrange(199)
        swap2 = stu_nums.pop(rand_index)
        room2 = swap2 // 4
        stu2 = swap2 % 4
        new_rooms = self.rooms
        temp_stu = new_rooms[room2][stu2]
        new_rooms[room2][stu2] = new_rooms[room1][stu1]
        new_rooms[room1][stu1] = temp_stu
        return new_rooms

    def __update_temperature(self):
        # updates temp according to cooling schedule
        if self.attempted_swaps % 20000 == 0:
            self.current_temp = self.current_temp * self.cooling
        elif self.actual_swaps % 2000 == 0:
            self.current_temp = self.current_temp * self.cooling

    def generate_swap(self):
        # gets a next state, compares to current state, and decides whether to move forward or not
        self.attempted_swaps += 1
        self.__update_temperature()
        swap_type = {
            0: self.__swap_single(),
            1: self.__swap_double()
        }
        new_rooms = swap_type[random.randrange(2)]
        new_fitness = self.__get_fitness_all(new_rooms)
        if new_fitness[0] < self.fitness_avg:
            # move to better fitness state
            debug = "~ better fitness accepted on attempt {:>9,} ~"
            self.rooms = new_rooms
            self.fitness_avg = new_fitness[0]
            self.fitness_high = new_fitness[1]
            self.fitness_low = new_fitness[2]
            self.actual_swaps += 1
            self.seq_non_swaps = 0
        elif E**((self.fitness_avg - new_fitness[0]) / self.current_temp) > random.random():
            # probability to accept worse state = E^(-delta/T)
            debug = "~ worse fitness accepted on attempt  {:>9,} ~"
            self.rooms = new_rooms
            self.fitness_avg = new_fitness[0]
            self.fitness_high = new_fitness[1]
            self.fitness_low = new_fitness[2]
            self.actual_swaps += 1
            self.seq_non_swaps = 0
        else:
            # no changes accepted
            debug = "~ no new fitness accepted on attempt {:>9,}  ~"
            self.seq_non_swaps += 1
        print(debug.format(self.attempted_swaps) + " " + str(self.fitness_avg))


initial_temp = 800
cooling = 0.95
E = 2.718281828459


def get_fitness_table():  # open file of match ratings and add to array
    fitness = [None] * 200
    try:
        fitness_data = open('roommates.txt')
    except FileNotFoundError:
        print("Can't find file, exiting")
        return 1

    index = 0
    temp = []
    for line in fitness_data:
        for rating in line.split():
            temp.append(int(rating))
        fitness[index] = temp
        index += 1

    fitness_data.close()
    return fitness


def main():

    solver = SimulateAnnealingTool()

    print("Fitness: {}".format(solver.fitness_avg))
    print(solver)
    # i = 0
    # while i < 5:
    #     solver.generate_swap()
    #     print(solver)
    #     i += 1

    start = time.time()
    while solver.seq_non_swaps < 20000:
        solver.generate_swap()
        # if solver.attempted_swaps % 2000 == 0:
        #     print(solver)
    stop = time.time()
    total_time = stop-start
    avg_time = total_time / solver.attempted_swaps
    print("~~~~~~~ The Final Results ~~~~~~~")
    print("20,000 iterations without changes")
    print("Total execution time: {}, average: {}s".format(total_time, avg_time))
    print(solver)
    solver.save_to_file()


if __name__ == '__main__':
    main()
