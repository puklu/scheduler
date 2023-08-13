import threading


class Resource:
    """
    Resource class representing an available resource for task allocation.

    This class manages the allocation and completion of tasks on a resource. Each resource can
    hold only one task at a time. The class provides methods to assign tasks to resources and
    mark tasks as completed when finished.

    Attributes:
        resource_id (int): The unique identifier for the resource.
        task (Task or None): The current task assigned to the resource, or None if no task is assigned.
        status (str): The status of the resource ("free" or "busy").
        lock (threading.Lock): A threading lock used for synchronization when assigning and removing tasks.

    Methods:
        assign_task(task: Task): Assigns a task to the resource and updates its status to "busy".
        remove_task(): Removes the assigned task from the resource and updates its status to "free"
            when the task is completed.

    Usage example:
        resource = Resource(resource_id=1)
        task = Task(task_id=1, project_id=0, priority=50)
        resource.assign_task(task)
        resource.remove_task()
    """
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.task = None
        self.status = "free"
        self.lock = threading.Lock()  # A lock for resource synchronization

    def assign_task(self, task):
        with self.lock:
            self.task = task
            self.status = "busy"
            print(f" RESOURCE: Task {task[1].task_id} of project {task[1].project_id} with priority {task[1].priority} allocated to resource {self.resource_id}")

    def remove_task(self):
        with self.lock:
            if self.task is not None:
                print(
                    f" \u2713 FINISHED: Task {self.task[1].task_id} of project {self.task[1].project_id} with priority {self.task[1].priority} finished at resource {self.resource_id}")
                self.task = None
                self.status = "free"
