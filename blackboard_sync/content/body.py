from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from blackboard.blackboard import BBCourseContent

from .base import FStream
from .job import DownloadJob
from .templates import create_body
from .webdav import WebDavFile, ContentParser


class ContentBody(FStream):
    """Process the content body to find WebDav files."""

    def __init__(self, content: BBCourseContent, _: None,
                 job: DownloadJob) -> None:
        self.ignore = False

        if not content.body:
            self.ignore = True
            return

        title = content.title or "Untitled"
        self.modified_time = content.modified_time if content else None
        parser = ContentParser(content.body, job.session.instance_url)

        self.body = create_body(title, parser.body, parser.text)
        self.children = [WebDavFile(ln, job) for ln in parser.links]

    def write(self, path: Path, executor: ThreadPoolExecutor) -> None:
        if self.ignore:
            return

        self.write_base(
            path / f"{path.stem}.html", executor, self.body, self.modified_time
        )

        for child in self.children:
            child.write(path, executor, self.modified_time)
