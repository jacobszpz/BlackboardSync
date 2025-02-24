import logging
from pathlib import Path
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor

from blackboard.blackboard import BBCourse

from .api_path import BBContentPath
from .job import DownloadJob
from .content import Content

logger = logging.getLogger(__name__)


class Course:
    def __init__(self, course: BBCourse, job: DownloadJob):
        logger.info(f"<{course.code}> - <{course.title}>")

        self.ignore = not course.availability

        if self.ignore:
            return

        self.year = self.get_year(course.created)
        self.title = course.title or 'Untitled Course'
        self.modified_time = course.modified

        contents = job.session.fetch_contents(course_id=course.id)
        self.children = []

        for content in contents:
            api_path = BBContentPath(course_id=course.id,
                                     content_id=content.id)
            self.children.append(Content(content, api_path, job))

    def write(self, path: Path, executor: ThreadPoolExecutor) -> None:
        if self.ignore:
            return

        path = path / self.year / self.title

        for child in self.children:
            child.write(path, executor)

        if self.modified_time:
            timestamp = self.modified_time.timestamp()
            path.touch(exist_ok=True)
            os.utime(path, (timestamp, timestamp))

    @staticmethod
    def get_year(created: datetime | None) -> str:
        return str(created.year) if created is not None else 'No Date'
