import unittest
import threading
import random

from src.Scheduler import Scheduler
from src.Task import Task


class TestScheduler(unittest.TestCase):
    def test_init(self):
        """
        Tests the init method of Scheduler.
        """
        num_resources = 1
        num_projects = 2
        scheduler = Scheduler(num_resources, num_projects)

        self.assertEqual(len(scheduler.resources), num_resources)
        self.assertEqual(len(scheduler.projects_queues), num_projects)

    def test_add_task(self):
        """
        Tests add_task method of Scheduler

        """
        task_id = 0
        project_id = 0
        priority = 5
        task = Task(task_id, project_id, priority)

        num_resources = 1
        num_projects = 1
        scheduler = Scheduler(num_resources, num_projects)
        scheduler.add_task(task)

        self.assertEqual(scheduler.projects_queues[project_id].get()[1], task)

    def test_allocate_resources(self):
        """
        Tests that available resource is allocated to a task.
        """
        num_resources = 2
        num_projects = 1
        scheduler = Scheduler(num_resources, num_projects)
        task = Task(task_id=1, project_id=0, priority=50)
        scheduler.add_task(task)
        resource = scheduler.resources[0]

        terminate_flag = threading.Event()
        allocate_thread = threading.Thread(target=scheduler.allocate_resources, args=(terminate_flag,))
        allocate_thread.start()

        terminate_flag.set()  # Set the flag to stop the loop
        allocate_thread.join()  # Wait for the thread to finish

        # Assert that the resource has been assigned the task
        self.assertEqual(resource.task[1], task)

    def test_allocate_resources2(self):
        """
        Tests that all projects are given equal resources irrespective of the length of their queue.
        """
        num_resources = 4
        num_projects = 2
        scheduler = Scheduler(num_resources, num_projects)

        # setting the number of tasks for each project
        num_tasks_in_each_project = [5, 1]
        cols = iter(num_tasks_in_each_project)

        # populating the projects' priority queues
        for p_id in range(num_projects):
            for t_id in range(next(cols)):
                priority = random.randint(1, 100)  # setting a random priority to each task
                task = Task(task_id=t_id, project_id=p_id, priority=priority)
                scheduler.add_task(task)

        # starting a new thread for the scheduler
        terminate_flag = threading.Event()
        allocate_thread = threading.Thread(target=scheduler.allocate_resources, args=(terminate_flag,))
        allocate_thread.start()

        terminate_flag.set()  # Set the flag to stop the loop
        allocate_thread.join()  # Wait for the thread to finish

        for k in range(min(num_projects, num_resources)):
            self.assertEqual(scheduler.resources[k].task[1].project_id, k)

    def test_allocate_resources3(self):
        """
        Tests that all projects are given equal resources irrespective of the length of their queue.
        """
        num_resources = 2
        num_projects = 2
        scheduler = Scheduler(num_resources, num_projects)

        task00 = Task(task_id=0, project_id=0, priority=6)
        task10 = Task(task_id=1, project_id=0, priority=2)
        task01 = Task(task_id=0, project_id=1, priority=60)

        scheduler.add_task(task00)
        scheduler.add_task(task10)
        scheduler.add_task(task01)

        # starting a new thread for the scheduler
        terminate_flag = threading.Event()
        allocate_thread = threading.Thread(target=scheduler.allocate_resources, args=(terminate_flag,))
        allocate_thread.start()
        terminate_flag.set()  # Set the flag to stop the loop
        allocate_thread.join()  # Wait for the thread to finish

        self.assertEqual(scheduler.resources[0].task[1].project_id, 0)
        self.assertEqual(scheduler.resources[1].task[1].project_id, 1)
        self.assertEqual(scheduler.resources[0].task[1].priority, 2)
        self.assertEqual(scheduler.resources[1].task[1].priority, 60)

    def test_remove_task(self):
        """
        Tests if a resource is freed up when remove_task is called.
        And then tests if the next task in queue is allocated to resource.
        """
        num_resources = 1
        num_projects = 1
        scheduler = Scheduler(num_resources, num_projects)

        task00 = Task(task_id=0, project_id=0, priority=6)
        task10 = Task(task_id=1, project_id=0, priority=2)  # this one should be assigned the resource first

        scheduler.add_task(task00)
        scheduler.add_task(task10)

        # starting a new thread for the scheduler
        terminate_flag = threading.Event()
        allocate_thread = threading.Thread(target=scheduler.allocate_resources, args=(terminate_flag,))
        allocate_thread.start()
        terminate_flag.set()  # Set the flag to stop the loop
        allocate_thread.join()  # Wait for the thread to finish

        self.assertEqual(scheduler.resources[0].task[1].project_id, 0)
        self.assertEqual(scheduler.resources[0].task[1].task_id, 1)  # the task with higher priority

        # remove the task from the resource
        scheduler.resources[0].remove_task()

        # check again
        self.assertEqual(scheduler.resources[0].task, None)
        self.assertEqual(scheduler.resources[0].status, "free")

        # allocate the resource to the next task in queue
        terminate_flag = threading.Event()
        allocate_thread = threading.Thread(target=scheduler.allocate_resources, args=(terminate_flag,))
        allocate_thread.start()
        terminate_flag.set()  # Set the flag to stop the loop
        allocate_thread.join()  # Wait for the thread to finish

        # the next task should have the resource
        self.assertEqual(scheduler.resources[0].task[1].project_id, 0)
        self.assertEqual(scheduler.resources[0].task[1].task_id, 0)  # the task with 2nd highest priority

        # remove the task from the resource
        scheduler.resources[0].remove_task()

        # check again
        self.assertEqual(scheduler.resources[0].task, None)
        self.assertEqual(scheduler.resources[0].status, "free")

    def test_no_tasks(self):
        """
        Tests the case when there are no tasks to allocate resources to.
        """
        num_resources = 1
        num_projects = 0

        scheduler = Scheduler(num_resources, num_projects)

        terminate_flag = threading.Event()
        allocate_thread = threading.Thread(target=scheduler.allocate_resources, args=(terminate_flag,))
        allocate_thread.start()
        terminate_flag.set()  # Set the flag to stop the loop
        allocate_thread.join()  # Wait for the thread to finish

        # resource should be free
        self.assertEqual(scheduler.resources[0].task, None)
        self.assertEqual(scheduler.resources[0].status, "free")  # the task with 2nd highest priority


if __name__ == "__main__":
    unittest.main()
