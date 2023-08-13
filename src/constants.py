"""
All the constants used in the project can be changed from here.
"""

# default values for number of resources available and number of projects
NUM_RESOURCES = 3
NUM_PROJECTS = 5

# A new task is generated/simulated between every TASK_GENERATION_LOW and TASK_GENERATION_HIGH seconds.
TASK_GENERATION_LOW = 2   # Lower limit of seconds at which a new task is generated
TASK_GENERATION_HIGH = 6  # Higher limit of seconds at which a new task is generated

# A new task is "completed" between every TASK_COMPLETION_LOW and TASK_COMPLETION_HIGH seconds.
TASK_COMPLETION_LOW = 5
TASK_COMPLETION_HIGH = 10

# A priority number between PRIORITY_LOW and PRIORITY_HIGH is randomly assigned to each task.
PRIORITY_LOW = 1
PRIORITY_HIGH = 100

# Number of tasks assigned to each project is between NUMBER_OF_TASKS_LOW and NUMBER_OF_TASKS_HIGH for
# sample_generate_tasks method
NUMBER_OF_TASKS_LOW = 1
NUMBER_OF_TASKS_HIGH = 7