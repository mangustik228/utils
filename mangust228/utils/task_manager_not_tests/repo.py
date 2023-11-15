from collections import Counter
import json

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from loguru import logger

from .db import get_session
from .models import TaskModel
from .task import Task


class TaskRepo:
    def __init__(self, retries: int):
        self._get_session = get_session
        self.retries = retries
        self.errors = Counter()

    def get_all(self, done: bool = False) -> list:
        stmt = select(TaskModel.id, TaskModel.url, TaskModel.retries)\
            .filter(TaskModel.retries < self.retries)\
            .filter(TaskModel.done == done)\
            .filter(TaskModel.reason.is_(None))
        with self._get_session() as session:
            urls = session.execute(stmt)
        return urls.fetchall()

    def _insert_one_task(self, session: Session, url: str):
        try:
            task = TaskModel(url=url)
            session.add(task)
            session.commit()
            return "success"
        except Exception as e:
            session.rollback()
            return str(type(e))

    def add_retry(self, id: int):
        with get_session() as session:
            task = self._get_model_task_by_id(session, id)
            task.retries += 1
            session.commit()
        return "success"

    def _get_model_task_by_id(self, session: Session, id: int):
        stmt = select(TaskModel).filter(TaskModel.id == id)
        task = session.execute(stmt)
        task = task.scalar()
        return task

    def get_by_id(self, id: int):
        with get_session() as session:
            task = self._get_model_task_by_id(session, id)
            task = Task(url=task.url, id=task.id)
        return task

    def confirm_parsing(self, id: int, result_url: str):
        with get_session() as session:
            task = self._get_model_task_by_id(session, id)
            task.done = True
            task.result_url = result_url
            session.commit()
        return "success"

    def insert_many_urls(self, urls: list[str]):
        for url in urls:
            if not url.startswith("http"):
                url = "https://" + url
            with get_session() as session:
                result = self._insert_one_task(session, url)
                if result != "success":
                    self.errors[result] += 1
        logger.warning(
            f'Не удалось вставить задачи: {json.dumps(self.errors, indent=4)}')

    def insert_one_url(self, url: str):
        with self._get_session() as session:
            self._insert_one_task(session, url)
            stmt = select(TaskModel.id, TaskModel.url)\
                .filter(TaskModel.url == url)
            result = session.execute(stmt)
        return result.mappings().all()[0]

    def insert_error_parsing(self, id: int, reason: str):
        with self._get_session() as session:
            stmt = update(TaskModel).filter(
                TaskModel.id == id).values(reason=reason)
            session.execute(stmt)
            session.commit()

    def update_retrieves(self):
        with self._get_session() as session:
            stmt = update(TaskModel).values(retries=0)
            session.execute(stmt)
            session.commit()
