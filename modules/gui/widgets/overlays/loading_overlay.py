from PySide6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class LoadingOverlay(QWidget):
    """Semi-transparent overlay shown while quiz questions are loading."""

    def __init__(self) -> None:
        super().__init__()
        self._setup_overlay()
        self._setup_layout()
        self._setup_loading_label()
        self._setup_progress_bar()

    def _setup_overlay(self) -> None:
        self.setObjectName("loadingOverlay")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

    def _setup_layout(self) -> None:
        self._main_layout = QVBoxLayout()
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._main_layout)

    def _setup_loading_label(self) -> None:
        self._label = QLabel(
            "Loading questions...",
            alignment=Qt.AlignmentFlag.AlignCenter
            )
        self._label.setObjectName("loadingOverlayLabel")

        self._main_layout.addWidget(self._label)

    def _setup_progress_bar(self):
        self._progress_bar = QProgressBar()
        self._progress_bar.setObjectName("loadingOverlayProgressBar")
        self._progress_bar.setRange(0, 0)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setFixedWidth(280)

        self._main_layout.addWidget(self._progress_bar)

    def show_loading(self):
        self.raise_()
        self.show()

    def hide_loading(self):
        self.hide()
