import csv
import sys
import random
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)
sys.argv += ['-platform', 'windows:darkmode=2']


def apply_dark_palette(app: QApplication) -> None:
    app.setStyle("Fusion")

    palette = QPalette()

    palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(230, 230, 230))
    palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(230, 230, 230))
    palette.setColor(QPalette.ColorRole.Text, QColor(230, 230, 230))
    palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(230, 230, 230))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 80, 80))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(150, 150, 150))

    app.setPalette(palette)
    app.setStyleSheet(
        """
        QWidget {
            background-color: #2d2d2d;
            color: #e6e6e6;
        }
        QLineEdit,
        QTextEdit,
        QPlainTextEdit,
        QComboBox,
        QSpinBox,
        QDoubleSpinBox,
        QDateEdit,
        QTimeEdit,
        QDateTimeEdit,
        QFontComboBox {
            background-color: #1f1f1f;
            color: #f0f0f0;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 4px 6px;
        }
        QComboBox::drop-down {
            border: none;
            width: 22px;
            background-color: #343434;
        }
        QComboBox QAbstractItemView {
            background-color: #1f1f1f;
            color: #f0f0f0;
            border: 1px solid #555;
            selection-background-color: #2a82da;
            selection-color: #ffffff;
        }
        QPushButton {
            background-color: #3a3a3a;
            color: #f0f0f0;
            border: 1px solid #5a5a5a;
            border-radius: 5px;
            padding: 6px 10px;
        }
        QPushButton:hover {
            background-color: #4a4a4a;
        }
        QPushButton:pressed {
            background-color: #2a82da;
            border-color: #2a82da;
        }
        QProgressBar {
            background-color: #1f1f1f;
            color: #f0f0f0;
            border: 1px solid #555;
            border-radius: 4px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #2a82da;
        }
        QToolTip {
            color: #e6e6e6;
            background-color: #2d2d2d;
            border: 1px solid #666;
        }
        """
    )


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Meridian")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox,
            QComboBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox,
            QLabel,
            QLCDNumber,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QRadioButton,
            QSlider,
            QSpinBox,
            QTimeEdit,
        ]

        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)



with open('subscriber-list.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        print(', '.join(row))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_palette(app)
    window = MyWidget()
    window.show()

    sys.exit(app.exec())