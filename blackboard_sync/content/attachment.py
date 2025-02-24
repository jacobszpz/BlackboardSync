import uuid
import mimetypes
from datetime import datetime

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from blackboard.blackboard import BBAttachment

from .base import BStream
from .api_path import BBContentPath
from .job import DownloadJob


class Attachment(BStream):
    """File attached to a content."""

    def __init__(
        self,
        attachment: BBAttachment,
        api_path: BBContentPath,
        job: DownloadJob,
        modified_time: datetime | None = None,
    ) -> None:
        filename = attachment.fileName or str(uuid.uuid1())
        name_ext = '.' + filename.split('.')[-1]

        # Guess extension based on content
        mime = attachment.mimeType or 'text/plain'
        possible_ext = mimetypes.guess_all_extensions(mime, strict=False)

        if name_ext in possible_ext:
            self.filename = filename
        else:
            real_ext = possible_ext[0] if possible_ext else '.txt'
            self.filename = filename + real_ext

        self.modified_time = modified_time

        self.stream = job.session.download(attachment_id=attachment.id,
                                           **api_path)

    def write(self, path: Path, executor: ThreadPoolExecutor) -> None:
        super().write_base(
            path / self.filename, executor, self.stream, self.modified_time
        )
