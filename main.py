import concurrent.futures
import threading
import argparse

from src.Scheduler import Scheduler
from src.simulators import generate_tasks, complete_tasks
from src.constants import NUM_PROJECTS, NUM_RESOURCES

terminate_flag = threading.Event()


def main():
    parser = argparse.ArgumentParser(description='Tool to schedule resources')
    parser.add_argument('-n', help="Number of resources available", default=NUM_RESOURCES)
    parser.add_argument('-p', help="Number of projects", default=NUM_PROJECTS)
    args = parser.parse_args()

    num_resources = int(args.n)
    num_projects = int(args.p)

    scheduler = Scheduler(num_resources, num_projects)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(scheduler.allocate_resources, terminate_flag)
        executor.submit(generate_tasks, num_projects, scheduler, terminate_flag)
        executor.submit(complete_tasks, scheduler, terminate_flag)

        try:
            executor.shutdown(wait=True)
        except KeyboardInterrupt:
            print("Program interrupted. Cleaning up threads...")
            terminate_flag.set()
            executor.shutdown(cancel_futures=False)
            print("Threads cleaned up. Exiting.")


if __name__ == '__main__':
    main()

    # scheduler = Scheduler(NUM_RESOURCES, NUM_PROJECTS)
    # sample_generate_tasks(NUM_PROJECTS, scheduler)
    # scheduler.allocate_resources()


