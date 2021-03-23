# simulated-annealing-project

Project tasks:

- set up general file structure in pycharm
- create function to read in file contents and save them to a variable in a useful way 
	- 2d array! rating[student1][student2] : relationship rating
- rate()  # create function to apply ratings to a designation state
- create function to apply changes -> 
	- this function should increment tested_states always
- create function to compare ratings and choose
	- this should increment accepted_states when switching states


class State - functionality should include:
	1. default constructor which defines class variables
	2. method for creating a new state  # gonna have to keep thinking on this one
	3. method for changing a state
		choose randomly between:
	 		Select 2 rooms at random, and 1 student at random from each room; exchange them. 
	 		Select 2 rooms at random; swap the first 2 students in one room with the last 2 students in the other. 
	4. method for calculating designation ratings
	5. 

