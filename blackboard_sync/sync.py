"""
BlackboardSync.

Automatically sync content from Blackboard
"""

# Copyright (C) 2023, Jacob Sánchez Pérez

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import time
import logging
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta

from requests.cookies import RequestsCookieJar
from requests.exceptions import ConnectionError

from .config import SyncConfig
from .download import BlackboardDownload
from .blackboard import BlackboardSession


class BlackboardSync:
    """Represents an instance of the BlackboardSync application."""

    _log_directory = "log"
    _app_name = 'blackboard_sync'

    # Filters out non-subjects from blackboard (may need more testing)
    _data_source = "_21_1"

    # Seconds between each check of time elapsed since last sync
    _check_sleep_time = 10
    # Sync thread max retries
    _max_retries = 3

    _logger = logging.getLogger(__name__)

    def __init__(self):
        """Create an instance of the program."""
        # Time between each sync in seconds
        self._sync_interval = 60 * 30

        # Time before last sync
        self._last_sync = None
        # Time of next programmed sync
        self._next_sync = None
        # User session active
        self._is_logged_in = False

        # Flag to force sync
        self._force_sync = False
        # Flag to know if syncing is in progress
        self._is_syncing = False
        # Flag to know if syncing is on
        self._is_active = False

        # Set up logging
        self._logger.setLevel(logging.WARN)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.debug("Initialising BlackboardSync")

        sess_logger = logging.getLogger("BlackboardSession")
        sess_logger.setLevel(logging.WARN)
        sess_logger.addHandler(logging.StreamHandler())

        download_logger = logging.getLogger("BlackboardDownload")
        download_logger.setLevel(logging.WARN)
        download_logger.addHandler(logging.StreamHandler())

        self.sess_logger = sess_logger
        self.download_logger = download_logger

        # Attempt to load existing configuration
        self._config = SyncConfig()

        if self._config.last_sync_time:
            self.logger.info("Preexisting configuration exists")
            self._update_next_sync()

    def auth(self, cookie_jar: RequestsCookieJar) -> bool:
        """Create a new Blackboard session with the given credentials.

        Will start syncing automatically if login successful.

        :param bool persistence: If true, login will be saved in the OS designated keyring.
        """
        self._cookies = cookie_jar

        try:
            u_sess = BlackboardSession(cookie_jar)
        except ValueError:
            self.logger.warning("Credentials are incorrect")
        else:
            self.logger.info("Logged in successfully")
            self.sess = u_sess
            self._is_logged_in = True
            self.start_sync()

        return self._is_logged_in

    def log_out(self) -> None:
        """Stop syncing and forget user session."""
        self.stop_sync()
        self.sess = None
        self._is_logged_in = False

    def _sync_task(self) -> None:
        """Constantly check if the data is outdated and if so start a download job.

        Method run by Sync thread.
        """
        reload_session = False
        failed_attempts = 0

        while self._is_active:
            if self.outdated or self._force_sync:
                self.logger.debug("Syncing now")
                self._is_syncing = True

                # Download from last datetime
                new_download = BlackboardDownload(self.sess, self.download_location / '', self.last_sync_time)

                try:
                    self.last_sync = new_download.download()
                    failed_attempts = 0
                except ValueError:
                    # Session expired, log out and attempt to reload config
                    self.logger.warning("User session expired")
                    reload_session = True
                    self.log_out()
                except ConnectionError as e:
                    # Random python connection error
                    self._log_exception(e)
                    failed_attempts += 1

                # Could not sync
                if failed_attempts >= self._max_retries:
                    self.log_out()

                # Reset force sync flag
                self._force_sync = False
                self._is_syncing = False
            time.sleep(self._check_sleep_time)

        if reload_session:
            self.auth(self._cookies)

    def start_sync(self) -> None:
        """Stars Sync thread."""
        self.logger.info("Starting sync thread")
        self._is_active = True
        self.sync_thread = threading.Thread(target=self._sync_task)
        self.sync_thread.start()

    def stop_sync(self) -> None:
        """Stop Sync thread."""
        self.logger.info("Stopping sync thread")
        self._is_active = False

    def _log_exception(self, e: Exception) -> None:
        """Log exception to log file inside sync location."""
        self._log_dir.mkdir(exist_ok=True, parents=True)
        exception_log = logging.FileHandler(self._log_path)
        self.logger.addHandler(exception_log)
        self.logger.exception("Exception in sync thread")
        self.logger.removeHandler(exception_log)

    def force_sync(self) -> None:
        """Force Sync thread to start download job ASAP."""
        self.logger.debug("Forced syncing")
        self._force_sync = True

    @property
    def username(self) -> str:
        return self.sess.username

    @property
    def _log_path(self) -> Path:
        filename = f"sync_error_{datetime.now():%Y-%m-%dT%H_%M_%S_%f}.log"
        return Path(self._log_dir / filename)

    @property
    def _log_dir(self) -> Path:
        return Path(self.download_location / self._log_directory)

    @property
    def last_sync_time(self) -> datetime:
        """Datetime right before last download job started."""
        return self._config.last_sync_time

    @last_sync_time.setter
    def last_sync_time(self, last_time: datetime):
        """Updates the last sync time recorded."""
        self._config.last_sync_time = last_time
        self._update_next_sync()

    def _update_next_sync(self) -> None:
        """Store a calculated datetime when next sync should take place."""
        self._next_sync = (self._config.last_sync_time +
                           timedelta(seconds=self._sync_interval))

    @property
    def next_sync(self) -> datetime:
        """Time when last sync will be outdated."""
        return self._next_sync

    @property
    def outdated(self) -> bool:
        """Return true if last download job is outdated."""
        if self._config.last_sync_time is None:
            return True
        return datetime.now(timezone.utc) >= self.next_sync

    @property
    def data_source(self) -> str:
        """Filter the modules to download."""
        # The default works in my testing. However, this might need tweaking for other users,
        # specially if used for different institutions than UCLan.
        return self._data_source

    @data_source.setter
    def data_source(self, d: str) -> None:
        self._data_source = d

    @property
    def download_location(self) -> Path:
        """Location to where all Blackboard content will be downloaded."""
        return self._config.download_location

    def change_download_location(self, new_dir: Path, redownload: bool = False) -> None:
        """Set new sync location.

        :param Path dir: The path of the sync dir.
        :param bool redownload: If true, ALL content will be re-downloaded to the new location.
        """
        if new_dir != self._config.download_location:
            # Update configuration
            self._config.download_location = new_dir

            if redownload:
                # Unset last sync time to fully download all files in new location
                self.last_sync_time = None

    @property
    def sync_interval(self) -> int:
        """Time to wait between download jobs."""
        return self._sync_interval

    @sync_interval.setter
    def sync_interval(self, p: int) -> None:
        self._sync_interval = p

    @property
    def is_active(self) -> bool:
        """Indicate the state of the sync thread."""
        return self._is_active

    @property
    def is_logged_in(self) -> bool:
        """Indicate if a user session is currently active."""
        return self._is_logged_in

    @property
    def is_syncing(self) -> bool:
        """Flag raised everytime a download job is running."""
        return self._is_syncing

    @property
    def logger(self) -> logging.Logger:
        """Logger for BlackboardSync, set at level WARN."""
        return self._logger
