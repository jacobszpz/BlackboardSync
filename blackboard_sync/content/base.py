import os
from datetime import datetime
from pathlib import Path
from requests import Response

from concurrent.futures import ThreadPoolExecutor


class BStream:
    """Base class for content that can be downloaded as a byte stream."""
    CHUNK_SIZE = 1024

    def write_base(
        self,
        path: Path,
        executor: ThreadPoolExecutor,
        stream: Response,
        modified_time: datetime | None = None
    ) -> None:
        """Schedule the write operation."""

        def _write() -> None:
            with path.open("wb") as f:
                for chunk in stream.iter_content(chunk_size=self.CHUNK_SIZE):
                    f.write(chunk)

            if modified_time is not None:
                timestamp = modified_time.timestamp()
                os.utime(path, (timestamp, timestamp))

        executor.submit(_write)


class FStream:
    """Base class for content that can be written as text."""

    def write_base(self, path: Path, executor: ThreadPoolExecutor,
                   body: str, modified_time: datetime | None = None) -> None:
        """Schedule the write operation."""

        def _write() -> None:
            with path.open('w', encoding='utf-8') as f:
                f.write(body)

            if modified_time is not None:
                timestamp = modified_time.timestamp()
                os.utime(path, (timestamp, timestamp))

        executor.submit(_write)
