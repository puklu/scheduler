import time
import random

from .Task import Task
from .constants import TASK_GENERATION_LOW, TASK_GENERATION_HIGH, TASK_COMPLETION_LOW, TASK_COMPLETION_HIGH, PRIORITY_LOW, PRIORITY_HIGH, NUMBER_OF_TASKS_LOW, NUMBER_OF_TASKS_HIGH


def generate_tasks(num_projects, scheduler, terminate_flag):
    """
    Simulates task arrival/generation. A random project_id (between 0 and num_projects) is generated and a task
    is assigned to it. The task_id's for every project starts from 0 and keep on incrementing as more
    tasks are generated for the project. A priority is randomly assigned to each task.
    :param num_projects: int: the total number of projects.
    :param scheduler: an instance of class Scheduler.
    :param terminate_flag: an instance of threading.Event(): to terminate the thread on KeyboardInterrupt.
    """
    tasks_count = {i: 0 for i in range(num_projects)}  # to keep track of the last task_id for each project

    while not terminate_flag.is_set():
        project_id = random.randint(0, num_projects-1)
        task_id = tasks_count[project_id]   # task_id available for the project
        tasks_count[project_id] += 1        # increasing the count for the next task_id
        priority = random.randint(PRIORITY_LOW, PRIORITY_HIGH)   # randomly assigning a priority
        task = Task(task_id, project_id, priority)
        scheduler.add_task(task)            # task added to the scheduler's queue for the project
        print(f" ~ NEW TASK: Task {task.task_id} for project {task.project_id} with priority {priority} generated.")
        time.sleep(random.uniform(TASK_GENERATION_LOW, TASK_GENERATION_HIGH))    # a new task is generated between
        # every TASK_GENERATION_LOW and TASK_GENERATION_HIGH secs


def complete_tasks(scheduler, terminate_flag):
    """
    Simulates the completion of tasks.
    Selects any of the resources randomly and frees by the removing its current task to make way for a new task.
    :param scheduler: an instance of class Scheduler.
    :param terminate_flag:  an instance of threading.Event(): to terminate the thread on KeyboardInterrupt.
    """
    while not terminate_flag.is_set():
        resource_to_select = random.choice(scheduler.resources)  # select a resource randomly
        resource_to_select.remove_task()
        time.sleep(random.uniform(TASK_COMPLETION_LOW, TASK_COMPLETION_HIGH))   # "completes" a task randomly between
        # every TASK_COMPLETION_LOW and TASK_COMPLETION_HIGH secs


def sample_generate_tasks(num_projects, scheduler):
    """
    Simulates task arrival/generation. Can be used for general testing. Randomly decides the number of tasks
    for each project. Randomly assigns a priority to each task. And then adds all the tasks to the scheduler's
    queues of each project.
    :param num_projects: int: the total number of projects.
    :param scheduler: an instance of class Scheduler.
    """
    # random number of task for each project
    cols = [random.randint(NUMBER_OF_TASKS_LOW, NUMBER_OF_TASKS_HIGH) for _ in range(num_projects)]
    cols = iter(cols)
    for i in range(num_projects):
        for j in range(next(cols)):
            priority = random.randint(PRIORITY_LOW, PRIORITY_HIGH)
            task = Task(j, i, priority)
            scheduler.add_task(task)
            print(f" ~ NEW TASK: Task {task.task_id} for project {task.project_id} with priority {priority} generated.")
