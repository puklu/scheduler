import queue
import threading
import time

from .Resource import Resource


class Scheduler:
    """
    Scheduler class for allocating tasks to resources based on project queues.

    This class manages the allocation of tasks from project queues to available resources.
    It maintains project queues with prioritized tasks and assigns tasks to resources based on their availability.
    The allocation process is designed to ensure fairness and efficient utilization of resources.

    Attributes:
        resources (list[Resource]): A list of Resource instances representing available resources.
        projects_queues (dict[int, queue.PriorityQueue]): A dictionary of project queues,
            where each project's queue contains prioritized tasks.
        lock (threading.Lock): A threading lock used for synchronization when allocating tasks.

    Methods:
        add_task(task: Task): Adds a task to the appropriate project's queue.
        allocate_resources(terminate_flag: threading.Event): Allocates tasks to resources
            based on project queue priorities and resource availability.

    Usage example:
        scheduler = Scheduler(num_resources=3, num_projects=5)
        scheduler.add_task(task)
        scheduler.allocate_resources(terminate_flag=threading.Event())
    """
    def __init__(self, num_resources, num_projects):
        self.resources = [Resource(i) for i in range(num_resources)]
        self.projects_queues = {i: queue.PriorityQueue() for i in range(num_projects)}  # PriorityQueue!!
        self.lock = threading.Lock()

    def add_task(self, task):
        self.projects_queues[task.project_id].put((task.priority, task))

    def allocate_resources(self, terminate_flag):
        while not terminate_flag.is_set():
            with self.lock:
                # all projects picked up one by one irrespective of the queue length
                for project_id, project_queue in self.projects_queues.items():
                    if not project_queue.empty():
                        for resource in self.resources:
                            if resource.status == "free":
                                task = project_queue.get()   # the task with the highest priority is picked!
                                resource.assign_task(task)
                                break
            time.sleep(1)
