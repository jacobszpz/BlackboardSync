import logging
import os
from pathlib import Path
from json import JSONDecodeError
from pydantic import ValidationError
from requests import RequestException
from concurrent.futures import ThreadPoolExecutor

from blackboard.blackboard import (
    BBCourseContent,
    BBResourceType,
    BBContentHandler
)
from blackboard.exceptions import BBBadRequestError, BBForbiddenError

from . import folder, document, externallink, body, unhandled

from .api_path import BBContentPath
from .job import DownloadJob

logger = logging.getLogger(__name__)


class Content:
    """Content factory for all types."""

    def __init__(self, content: BBCourseContent, api_path: BBContentPath,
                 job: DownloadJob) -> None:

        logger.info(f"{content.title}[{content.contentHandler}]")

        self.body = None
        self.handler = None

        self.ignore = not Content.should_download(content, job)

        if self.ignore:
            return

        Handler = Content.get_handler(content.contentHandler)
        self.title = content.title_path_safe.replace('.', '_')
        self.modified_time = content.modified if content else None

        try:
            self.handler = Handler(content, api_path, job)
        except (ValidationError, JSONDecodeError,
                BBBadRequestError, BBForbiddenError):
            logger.exception(f"Error fetching {content.title}")

        try:
            if content.body:
                self.body = body.ContentBody(content, None, job)
        except (ValidationError, JSONDecodeError,
                BBBadRequestError, BBForbiddenError, RequestException):
            logger.warning(f"Error fetching body of {content.title}")

    def write(self, path: Path, executor: ThreadPoolExecutor) -> None:
        if self.ignore:
            return

        # Build nested path with content title
        path = path / self.title

        if self.handler is not None:
            if self.handler.create_dir:
                path.mkdir(exist_ok=True, parents=True)

            self.handler.write(path, executor)

        if self.body is not None:
            path.mkdir(exist_ok=True, parents=True)
            self.body.write(path, executor)

        if (self.modified_time and
                (self.handler is not None or self.body is not None)):
            timestamp = self.modified_time.timestamp()
            path.touch(exist_ok=True)
            os.utime(path, (timestamp, timestamp))

    @staticmethod
    def should_download(content: BBCourseContent, job: DownloadJob) -> bool:
        or_guards = [
            job.has_changed(content.modified),
            content.hasChildren,
        ]

        return any(or_guards) and bool(content.availability)

    @staticmethod
    def get_handler(content_handler: BBContentHandler | None):
        match content_handler:
            case BBResourceType.Folder | BBResourceType.Lesson:
                return folder.Folder
            case BBResourceType.File | BBResourceType.Document:
                return document.Document
            case BBResourceType.Assignment:
                return document.Document
            case BBResourceType.ExternalLink:
                return externallink.ExternalLink
            case _:
                return unhandled.Unhandled
