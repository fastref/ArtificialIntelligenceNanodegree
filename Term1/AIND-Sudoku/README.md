# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In constraint propagation you try to reduce the search space. For the naked twin problem you search in the first step two boxes 
in an unit with exactly two remaining possibilities that are the same, e.g. in unit [A1, A2, ..., A9] we may have in A1: 34 and
A6: 34. When we have found such a pair, we eliminate the values from that naked twins from the remaining boxes in that unit. Let' s have a look at 
the above example with A1: 34 and A6: 34. Assume we have in A9: 456. Then we can eliminate in A9 the value 4. Why? Let's do a proof to the contrary.
Assume, we set A9 to the value 4, then the value 4 is consumed and cannot be used anymore in A1 and A6. So, we have for boxes A3 and A6 the value 3
available. As each value in each box has to be unique and we just have one value for two boxes, we are now not able to solve this sudoku. So, setting 
the value 4 to A9 lead to a not solvable sudoku. From that we can conclude that we can delete value 4 from box A9.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In a diagonal sudoku we have two additional constraints compared to standard sudoko. Additionally, in each of the two 
diagonal lines of our sudoku field, we have to satisfy that each number 1 to 9 appear exactly one time. This is achieved
 by adding the two diagonal units (A1, B2, C3, ..., I) and (I1, H2, ..., A9) as a list to the so far used units. When 
 then our possibility reduction routines (elimination, only_choice, and naked_twins) are applied. In this routines the 
 possibilities are eliminated for each unit in our unit list that includes the diagonal constraint. By checking this 
all units we ensure that the constraint that in each unit each number 1 to 9 just appear one time guaranteed. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing
To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

