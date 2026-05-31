from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, QThread

if TYPE_CHECKING:
    from .question_loader import QuestionLoader

logger = logging.getLogger(__name__)


class WorkerThreadControllerError(Exception):
    """Raised when WorkerThreadController returns error."""


class WorkerThreadController(QObject):
    """
    Own and manage a QThread for a single worker object.

    The controller moves the worker to a background thread, connects the worker
    and thread lifecycle signals, starts the thread, and schedules Qt cleanup
    with deleteLater after the worker finishes.
    """

    thread_started = Signal()
    thread_finished = Signal()
    thread_error = Signal(WorkerThreadControllerError)

    def __init__(self, worker: QuestionLoader) -> None:
        super().__init__()
        self._running = False
        self._is_setup = False
        self._worker = worker
        self._worker_thread = QThread()

    def _setup_worker_thread(self) -> None:
        """Setup thread and worker."""
        self._worker.moveToThread(self._worker_thread)

    def _connect_signals(self) -> None:
        self._worker_thread.started.connect(self._on_thread_started)
        self._worker_thread.started.connect(self.thread_started.emit)
        self._worker_thread.started.connect(self._worker.run)

        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.finished.connect(self._worker_thread.quit)

        self._worker_thread.finished.connect(self._on_thread_finished)
        self._worker_thread.finished.connect(self.thread_finished.emit)
        self._worker_thread.finished.connect(self._worker_thread.deleteLater)

    def setup(self):
        """Setup thread and worker. Connects signals."""
        if self._is_setup:
            return
        self._setup_worker_thread()
        self._connect_signals()
        self._is_setup = True

    def _on_thread_started(self) -> None:
        logger.debug("Worker thread started for %s.", type(self._worker).__name__)
        self._running = True

    def _on_thread_finished(self) -> None:
        logger.debug("Worker thread finished for %s.", type(self._worker).__name__)
        self._running = False

    def run_thread(self) -> None:
        try:
            if self._is_setup is False:
                self.setup()
            self._worker_thread.start()
        except Exception as error:
            logger.exception("Failed to start worker thread.")
            self.thread_error.emit(WorkerThreadControllerError(str(error)))

    @property
    def is_running(self) -> bool:
        return self._running
    
    def stop(self) -> None:
        """
        Request the worker thread to stop and quit its event loop.

        This does not forcibly terminate running Python code. The thread stops
        cleanly once the worker returns control to the Qt event loop.
        """
        if self._worker_thread.isRunning():
            logger.info("Worker thread stop requested.")
            # requests interruption flag, so worker can react when it regains control
            self._worker_thread.requestInterruption()
            # Quit thread event loop
            self._worker_thread.quit()
        else:
            logger.debug("Worker thread stop ignored because thread is not running.")
