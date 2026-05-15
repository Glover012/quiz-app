from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QTimer

from ....questions import OpenTriviaClientError


class ErrorOverlay(QWidget):
    """
    Transparent overlay, that shows error label temporarily.
    Used for API and thread error displaying.
    """
    
    def __init__(self) -> None:
        super().__init__()
        self._setup_overlay()
        self._setup_layout()
        self._setup_label()
        self._setup_timer()

    def _setup_overlay(self) -> None:
        self.setObjectName("errorOverlay")
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def _setup_label(self) -> None:
        self.error_label = QLabel(
            alignment=Qt.AlignmentFlag.AlignCenter,
            wordWrap=True,
            )
        self.error_label.setObjectName('errorOverlayLabel')
        self.error_label.hide()

        self.main_layout.addWidget(
            self.error_label,
            alignment=Qt.AlignmentFlag.AlignTop
            )

    def _setup_timer(self) -> None:
        self.timer = QTimer(singleShot=True)
        self.timer.timeout.connect(self._hide_error_overlay)

    def show_error(
            self,
            error: Exception,
            for_seconds: int
            ) -> None:
        label_text = str(error)
        if type(error) is OpenTriviaClientError:
            label_text += " Try again in a few seconds."
        self.error_label.setText(label_text)
        self.error_label.update()
        self.raise_()
        self.show()
        self.error_label.show()
        if self.timer.isActive():
            self.timer.stop()
        self.timer.start(int(for_seconds*1000))

    def _hide_error_overlay(self) -> None:
        self.hide()
        self.error_label.hide()
