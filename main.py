import csv
import sys
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
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
        QTableWidget {
            background-color: #1f1f1f;
            color: #f0f0f0;
            border: 1px solid #555;
            gridline-color: #3b3b3b;
            selection-background-color: #2a82da;
            selection-color: #ffffff;
        }
        QHeaderView::section {
            background-color: #343434;
            color: #f0f0f0;
            border: 1px solid #555;
            padding: 6px;
            font-weight: 600;
        }
        """
    )


def read_subscribers_csv(path: str) -> tuple[list[str], list[list[str]]]:
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    if not rows:
        return [], []

    headers = rows[0]
    data_rows = rows[1:]
    return headers, data_rows


class MyWidget(QMainWindow):
    def __init__(self, headers: list[str], rows: list[list[str]]):
        super().__init__()

        self.setWindowTitle("Meridian Subscribers")
        self.resize(1000, 640)

        layout = QVBoxLayout()
        summary = QLabel(f"Loaded {len(rows)} subscribers")
        layout.addWidget(summary)

        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setRowCount(len(rows))
        table.setHorizontalHeaderLabels(headers)

        for row_index, row in enumerate(rows):
            for column_index, value in enumerate(row):
                table.setItem(row_index, column_index, QTableWidgetItem(value))

        table.resizeColumnsToContents()
        layout.addWidget(table)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_palette(app)
    csv_headers, csv_rows = read_subscribers_csv("subscriber-list.csv")
    window = MyWidget(csv_headers, csv_rows)
    window.show()

    sys.exit(app.exec())