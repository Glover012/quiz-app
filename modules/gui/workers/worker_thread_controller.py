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
    Run QThread for one worker and clean it up after completion. 
    Emit thread related signals.
    """

    thread_started = Signal()
    thread_finished = Signal()
    thread_error = Signal(WorkerThreadControllerError)

    def __init__(self, worker: QuestionLoader) -> None:
        super().__init__()
        self.running = False
        self.worker = worker
        self.worker_thread = QThread()
        self._setup_worker_thread()
        self._connect_signals()

    def _setup_worker_thread(self) -> None:
        """Setup thread and worker."""
        self.worker.moveToThread(self.worker_thread)

    def _connect_signals(self):
        self.worker_thread.started.connect(self._on_thread_started)
        self.worker_thread.started.connect(self.thread_started.emit)
        self.worker_thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.worker_thread.quit)

        self.worker_thread.finished.connect(self._on_thread_finished)
        self.worker_thread.finished.connect(self.thread_finished.emit)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

    def _on_thread_started(self) -> None:
        logger.debug("Worker thread started for %s.", type(self.worker).__name__)
        self.running = True

    def _on_thread_finished(self) -> None:
        logger.debug("Worker thread finished for %s.", type(self.worker).__name__)
        self.running = False

    def run_thread(self) -> None:
        try:
            self.worker_thread.start()
        except Exception as error:
            logger.exception("Failed to start worker thread.")
            self.thread_error.emit(WorkerThreadControllerError(str(error)))

    def is_running(self) -> bool:
        return self.running
    
    def stop(self) -> None:
        """Interrupt and quit thread."""
        if self.worker_thread.isRunning():
            logger.info("Worker thread stop requested.")
            # requests interruption flag, so worker can react when it regains control
            self.worker_thread.requestInterruption()
            # Quit thread event loop
            self.worker_thread.quit()
        else:
            logger.debug("Worker thread stop ignored because thread is not running.")
