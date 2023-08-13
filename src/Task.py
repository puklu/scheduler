class Task:
    """
    Task class represents a task to be allocated to a resource.

    This class defines a task with a unique task identifier, associated project identifier,
    and a priority value. Tasks are added to project queues and allocated to resources
    based on their priority.

    Attributes:
        task_id (int): The unique identifier for the task.
        project_id (int): The project identifier to which the task belongs.
        priority (int): The priority value of the task, used for task allocation.

    Usage example:
        task = Task(task_id=1, project_id=0, priority=50)
    """
    def __init__(self, task_id, project_id, priority):
        self.task_id = task_id
        self.project_id = project_id
        self.priority = priority
