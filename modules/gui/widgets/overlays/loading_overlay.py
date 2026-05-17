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
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

    def _setup_loading_label(self) -> None:
        self.label = QLabel(
            "Loading questions...",
            alignment=Qt.AlignmentFlag.AlignCenter
            )
        self.label.setObjectName("loadingOverlayLabel")

        self.main_layout.addWidget(self.label)

    def _setup_progress_bar(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("loadingOverlayProgressBar")
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedWidth(280)

        self.main_layout.addWidget(self.progress_bar)

    def show_loading(self):
        self.raise_()
        self.show()

    def hide_loading(self):
        self.hide()
