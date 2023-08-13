# Load balancing task scheduler
This tool implements a resource allocation system where tasks from different 
projects are efficiently allocated to available resources based on 
priorities. 

Each resource executes 1 task and the resource is fully occupied until this
task is completed.
Scheduler balances the computational resources to all projects equally
(regardless of queue length, lots of activity on one project does not clog the
processing of others)

## Priority Functionality
Tasks are allocated based on their assigned priorities. The scheduling algorithm ensures 
that higher-priority tasks are given precedence over lower-priority tasks. 
This feature ensures that critical tasks are completed in a timely manner, maintaining efficient resource utilization.

## Equal Project Importance
To prevent any single project from disproportionately hogging resources, 
the scheduler equally distributes resources among all projects. 
This approach ensures that every project receives fair access to 
available resources, regardless of the number of tasks or their durations.

## Usage
1. Navigate to the project folder.
2. Open the terminal in the current directory and run:

         python main.py -n <number-of-resources> -p <number-of-projects>


The tool accepts the following parameters:
     
           1. `-n`: Total number of resources available.

           2. `-p`: Total number of projects.
   
                  Default location is the root of this project if not provided by the user.

Both of the parameters are optional but recommended based on the use case.
The default values are `n=3` and `p=5` which can be changed in file `src/constants.py`

Example 1: For
        `Number of resources = 12`
        `Number of projects = 50`

         python3 main.py -n 12 -p 50

Example 2: This will run the program with default values:
            `Number of resources = 3`
            `Number of projects = 5`

         python3 main.py

## Task simulation
Arrival of tasks and completion of tasks has been simulated to verify 
the functionality.
Tasks are generated randomly with a random number denoting its priority.
Tasks are also completed randomly for simulation.


## Testing
To run the unit tests:

1. Navigate to the project folder.

2. Execute the test_all.py script:

       python3 test_all.py

### Stopping the Program
The program can be stopped by sending an interrupt signal using 
Ctrl + C in the terminal where it is running. Upon receiving the 
interrupt signal, the program will gracefully terminate and clean 
up any resources that were in use.