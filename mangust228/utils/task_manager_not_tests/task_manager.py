from queue import Queue

from loguru import logger
import pandas as pd
from sqlalchemy import update

from .repo import TaskRepo
from .task import Task


class TaskManager:
    def __init__(self, path: str, column_name: str = "url", max_retries: int = 5):
        self.max_retries = max_retries
        self.task_repo = TaskRepo(5)
        self._tasks: Queue[Task] = Queue()
        self.errors = 0
        self.completed = 0
        self._prepare_urls(path, column_name)
        logger.info(f'Created TaskManager')

    def print_stats(self):
        logger.debug(
            f'Success: {self.completed} | Errors: {self.errors}')

    def _prepare_urls(self, path: str, column_name: str):
        urls_from_file = pd.read_csv(path)[column_name].to_list()
        logger.info(f'file success readed')
        self.task_repo.insert_many_urls(urls_from_file)
        logger.info(f'urls inserted to database')
        urls = self.task_repo.get_all(done=False)
        logger.info(f'got all urls from database')
        for id, url, retries in urls:
            task = Task(url=url, id=id, retries=retries)
            self._tasks.put(task)
        logger.info(
            f'Success prepared urls, approximate size: {self._tasks.qsize()}')

    def get_task(self, timeout: int | float = 2) -> Task:
        return self._tasks.get(timeout=timeout)

    def return_task(self, task: Task) -> None:
        assert isinstance(task, Task)
        logger.info(f'returned task: {task}')
        self.task_repo.add_retry(task.id)
        task.retries += 1
        if task.retries < self.max_retries:
            self._tasks.put(task)
        else:
            logger.warning(f'task was retries more then {self.max_retries}')
        self.errors += 1

    def put_task(self, task: Task) -> None:
        assert isinstance(task, Task)
        self._tasks.put(task)

    def confirm_task(self, task: Task) -> None:
        assert isinstance(task, Task)
        self.completed += 1
        result = self.task_repo.confirm_parsing(task.id, task.result_url)
        if result == "success":
            return True

    def error_task(self, task: Task, reason: str):
        assert isinstance(task, Task)
        self.errors += 1
        logger.warning(f"{task} | {reason = }")
        self.task_repo.insert_error_parsing(task.id, reason)

    @property
    def not_empty(self):
        return self._tasks.not_empty
