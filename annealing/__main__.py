import random
import datetime
import time


class SimulateAnnealingTool:
    def __init__(self):
        self.rooms = []
        self.fitness_table = []
        self.curr_fit_avg = 0
        self.curr_fit_high = 0
        self.curr_fit_low = 600
        self.curr_fit_total = 0
        self.old_fit_avg = 0
        self.attempted_swaps = 0
        self.actual_swaps = 0
        self.seq_non_swaps = 0
        self.current_temp = initial_temp
        self.cooling = cooling
        self.equal_states = 0
        self.room_nums = []
        for i in range(50):
            self.room_nums.append(i)
        self.stu_nums = []
        for i in range(200):
            self.stu_nums.append(i)
        self.__create_fitness_table()
        self.__create_state()

    def __create_state(self):
        # sets up initial room designation and gets room scores
        temp_rooms = []  # empty array for room assignments
        for i in range(200):
            temp_rooms.append(i)
        random.shuffle(temp_rooms)  # randomize order
        for a, b, c, d in zip(*[iter(temp_rooms)] * 4):
            # subdivide into rooms of 4 with initial score
            room_score = 0
            room_score += self.fitness_table[a][b]
            room_score += self.fitness_table[a][c]
            room_score += self.fitness_table[a][d]
            room_score += self.fitness_table[b][c]
            room_score += self.fitness_table[b][d]
            room_score += self.fitness_table[c][d]
            temp = [a, b, c, d, room_score]
            self.rooms.append(temp)
            if room_score > self.curr_fit_high:
                self.curr_fit_high = room_score
            if room_score < self.curr_fit_low:
                self.curr_fit_low = room_score
            self.curr_fit_total += room_score
            self.curr_fit_avg = self.curr_fit_total / len(self.rooms)

    def __create_fitness_table(self):
        # open file of match ratings and add to array
        try:
            fitness_data = open('roommates.txt')
        except FileNotFoundError:
            print("Can't find file, exiting")
            return 1

        for line in fitness_data:
            temp = []
            for val in line.split():
                temp.append(int(val))
            self.fitness_table.append(temp)

        fitness_data.close()

    def __update_fitness(self, room1, room2):
        # updates all fitness scores for this state
        # takes input for the 2 rooms that were swapped for max efficiency
        for room in room1, room2:
            a = self.rooms[room][0]
            b = self.rooms[room][1]
            c = self.rooms[room][2]
            d = self.rooms[room][3]
            room_score = 0
            room_score += self.fitness_table[a][b]
            room_score += self.fitness_table[a][c]
            room_score += self.fitness_table[a][d]
            room_score += self.fitness_table[b][c]
            room_score += self.fitness_table[b][d]
            room_score += self.fitness_table[c][d]
            self.curr_fit_total -= self.rooms[room][4]
            self.curr_fit_total += room_score
            self.rooms[room][4] = room_score
            self.curr_fit_avg = self.curr_fit_total / len(self.rooms)

    def __update_hi_lo_fitness(self):
        # updates highest and lowest fitness for current state
        high = 0
        low = 600
        for room in self.rooms:
            fitness = room[4]
            if fitness < low:
                low = fitness
            if fitness > high:
                high = fitness
            self.curr_fit_low = low
            self.curr_fit_high = high

    def __sort_rooms(self):
        # sort rooms by student num, then sort room list
        for index in range(len(self.rooms)):
            score = self.rooms[index].pop(4)  # remove score and room number then re-append
            self.rooms[index].sort()
            self.rooms[index].append(score)
        self.rooms = sorted(self.rooms, key=lambda x: x[0])

    def __get_stats_template(self):
        # returns a formatted string of various info about the current state of the object
        temp_str = "Initial temperature: {}   Ending temperature: {:.3f}\n".format(initial_temp, self.current_temp)
        cool_str = "Cooling schedule: T = {}T after 2000 swaps or 20000 attempts\n".format(self.cooling)
        swap_str = "Attempted swaps: {:,}   Actual swaps: {:,}\n".format(self.attempted_swaps, self.actual_swaps)
        fit_str = """
            Average room fitness: {}
            Worst room fitness  : {}
            Best room fitness   : {}
            \n""".format(self.curr_fit_avg, self.curr_fit_high, self.curr_fit_low)
        return temp_str + cool_str + swap_str + fit_str

    def __get_rooms_template(self):
        # returns a formatted string of current room state
        rooms_str = "Each line below is a single room assignment\n"
        for room in self.rooms:
            rooms_str += "Students: {:>3}, {:>3}, {:>3}, {:>3};   Room Fitness: {:>3}\n".format(
                room[0], room[1], room[2], room[3], room[4])
        return rooms_str

    def __update_temperature(self):
        # updates temp according to cooling schedule
        if self.attempted_swaps % 20000 == 0 or (self.actual_swaps > 0 and self.actual_swaps % 2000 == 0):
            self.current_temp = self.current_temp * cooling

    def __get_rands_in_rooms(self):
        room1 = self.room_nums.pop(random.randrange(50))
        room2 = self.room_nums[random.randrange(49)]
        self.room_nums.insert(room1, room1)
        return room1, room2

    def __get_rands_in_students(self):
        swap1 = self.stu_nums.pop(random.randrange(200))
        swap2 = self.stu_nums[random.randrange(199)]
        self.stu_nums.insert(swap1, swap1)
        return swap1, swap2

    def __do_double_swap(self, room1, room2):
        # swap first 2 students in one random room with last 2 students in another room
        temp_stu = [self.rooms[room2][0], self.rooms[room2][1]]
        self.rooms[room2][0] = self.rooms[room1][2]
        self.rooms[room2][1] = self.rooms[room1][3]
        self.rooms[room1][2] = temp_stu[0]
        self.rooms[room1][3] = temp_stu[1]
        self.old_fit_avg = self.curr_fit_avg
        self.__update_fitness(room1, room2)

    def __do_single_swap(self, swap1, swap2):
        # swap one random student in a random room with one random student in another room
        room1 = swap1 // 4
        stu1 = swap1 % 4
        room2 = swap2 // 4
        stu2 = swap2 % 4
        temp_stu = self.rooms[room2][stu2]
        self.rooms[room2][stu2] = self.rooms[room1][stu1]
        self.rooms[room1][stu1] = temp_stu
        self.old_fit_avg = self.curr_fit_avg
        self.__update_fitness(room1, room2)

    def __switching_states(self):
        # uses simulated annealing to explore the area without getting stuck on a local minimum,
        # decreasing frequency of worse state changes over time
        # only returns false if new state is both worse and gets rejected
        if self.curr_fit_avg == self.old_fit_avg:
            # swap resulted in no change in fitness
            self.seq_non_swaps += 1
            self.equal_states += 1
            return True
        elif self.curr_fit_avg < self.old_fit_avg:
            # move to better fitness state
            self.actual_swaps += 1
            self.seq_non_swaps = 0
            return True
        elif E ** ((self.old_fit_avg - self.curr_fit_avg) / self.current_temp) > random.random():
            # probability to accept worse state = E^(-delta/T)
            self.actual_swaps += 1
            self.seq_non_swaps = 0
            return True
        else:
            # no changes accepted
            self.seq_non_swaps += 1
            return False

    def next_state(self):
        # moves to next state, runs checks w/simulated annealing, and returns state back if not switching
        self.attempted_swaps += 1
        self.__update_temperature()
        # choose random swap type
        choice = random.randrange(2)
        if choice == 0:
            # switch 2 random students
            [swap1, swap2] = self.__get_rands_in_students()
            self.__do_single_swap(swap1, swap2)
            if not self.__switching_states():
                # new state was not accepted, revert
                self.__do_single_swap(swap1, swap2)
        else:
            # switch 4 students from 2 random rooms
            [swap1, swap2] = self.__get_rands_in_rooms()
            self.__do_double_swap(swap1, swap2)
            if not self.__switching_states():
                # new state was not accepted, revert
                self.__do_double_swap(swap1, swap2)

    def __str__(self):
        # print function to provide nice output for debugging
        self.__sort_rooms()
        self.__update_hi_lo_fitness()
        return self.__get_stats_template() + self.__get_rooms_template()

    def save_to_file(self):
        # writes stats and room state to file
        self.__sort_rooms()
        self.__update_hi_lo_fitness()
        file_name = "results_{}.txt".format(datetime.datetime.now().strftime("%y%j%H%M%S"))
        output_file = open(file_name, 'w')
        output_file.writelines([self.__get_stats_template(), self.__get_rooms_template()])
        output_file.close()


initial_temp = 1000
cooling = 0.95
E = 2.718281828459


def main():

    times = []
    final_scores = []
    attempted_swaps = []
    loop_count = 20
    for loops in range(loop_count):
        solver = SimulateAnnealingTool()
        start = time.time()
        print("~ thinking... ~")
        while solver.seq_non_swaps < 20000:
            solver.next_state()
            # if solver.attempted_swaps % 2000 == 0:
            #     print(solver)
        stop = time.time()
        total_time = stop-start
        avg_time = total_time / solver.attempted_swaps
        print("~~~~~~~ The Final Results ~~~~~~~")
        print("20,000 iterations without changes")
        print("Total execution time: {:.3f}s, average: {:.6f}s".format(total_time, avg_time))
        print(solver)
        times.append(total_time)
        final_scores.append(solver.curr_fit_avg)
        attempted_swaps.append(solver.attempted_swaps)
        solver.save_to_file()
    agg_total_times = 0
    for mytime in times:
        agg_total_times += mytime
    agg_final_scores = 0
    for score in final_scores:
        agg_final_scores += score
    agg_attempted_swaps = 0
    for swap in attempted_swaps:
        agg_attempted_swaps += swap
    print("avg time: %s" % (agg_total_times / loop_count))
    print("avg scores: %s" % (agg_final_scores / loop_count))
    print("avg attempts: %s" % (agg_attempted_swaps / loop_count))


if __name__ == '__main__':
    main()
