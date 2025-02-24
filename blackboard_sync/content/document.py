import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from blackboard.blackboard import BBCourseContent
from blackboard.filters import BBAttachmentFilter
from bwfilters import BWFilter

from .attachment import Attachment
from .api_path import BBContentPath
from .job import DownloadJob


class Document:
    """Represents a file with attachments in the Blackboard API"""
    def __init__(self, content: BBCourseContent, api_path: BBContentPath,
                 job: DownloadJob):
        attachments = job.session.fetch_file_attachments(**api_path)
        assert isinstance(attachments, list)

        att_filter = BBAttachmentFilter(mime_types=BWFilter(['video/*']))
        filtered_attachments = list(att_filter.filter(attachments))

        self.attachments = []
        self.modified_time = content.modified if content else None

        for i, attachment in enumerate(filtered_attachments):
            self.attachments.append(
                Attachment(
                    attachment, api_path, job, modified_time=self.modified_time
                )
            )

    def write(self, path: Path, executor: ThreadPoolExecutor) -> None:
        # If only attachment, just use parent
        if len(self.attachments) > 1:
            path.mkdir(exist_ok=True, parents=True)
        else:
            path = path.parent

        for attachment in self.attachments:
            attachment.write(path, executor)

        if self.modified_time and self.attachments:
            timestamp = self.modified_time.timestamp()
            path.touch(exist_ok=True)
            os.utime(path, (timestamp, timestamp))

    @property
    def create_dir(self) -> bool:
        return False
