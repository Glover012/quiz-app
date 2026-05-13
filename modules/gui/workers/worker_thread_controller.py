from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot, QThread

if TYPE_CHECKING:
    from .question_loader import QuestionLoader


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
        self.worker = worker
        self.worker_thread = QThread()
        self._setup_thread()

    def _setup_thread(self) -> None:
        """Setup thread and worker."""
        # Worker
        self.worker.moveToThread(self.worker_thread)
        # Quit thread when worker finish job to
        # ensure the thread emits finished so cleanup func runs
        self.worker.finished.connect(self.worker_thread.quit)
        # Thread
        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.started.connect(self.thread_started.emit)
        self.worker_thread.finished.connect(self._clean)
        self.worker_thread.finished.connect(self.thread_finished.emit)

    def run_thread(self) -> None:
        """
        Run thread. When worker emits finished, quit thread 
        and perform cleanup procedure.
        """
        try:
            self.worker_thread.start()
        except Exception as error:
            self.thread_error.emit(WorkerThreadControllerError(str(error)))

    @Slot()
    def _clean(self) -> None:
        """Remove thread and worker."""
        self.worker.deleteLater()
        self.worker_thread.deleteLater()
