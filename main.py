import csv
import sys
from datetime import datetime
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
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
            font-family: Segoe UI;
            font-size: 12px;
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
        QFrame#TopPanel {
            background-color: #262626;
            border: 1px solid #3f3f3f;
            border-radius: 10px;
        }
        QLabel#TitleLabel {
            font-size: 20px;
            font-weight: 700;
            color: #ffffff;
        }
        QLabel#SubTitleLabel {
            color: #bfbfbf;
        }
        QLabel#SummaryLabel {
            color: #d8d8d8;
            font-weight: 600;
        }
        QTableWidget {
            background-color: #1f1f1f;
            color: #f0f0f0;
            border: 1px solid #555;
            gridline-color: #3b3b3b;
            selection-background-color: #2a82da;
            selection-color: #ffffff;
        }
        QTableWidget::item {
            padding: 4px;
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


def parse_subscribe_date(raw_value: str) -> tuple[str, str, str]:
    if not raw_value:
        return "", "", ""

    try:
        dt = datetime.fromisoformat(raw_value.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S"), dt.strftime("%a")
    except ValueError:
        return raw_value, "", ""


def enrich_subscribe_date(headers: list[str], rows: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    if "Subscribe Date" not in headers:
        return headers, rows

    subscribe_index = headers.index("Subscribe Date")

    enriched_headers: list[str] = []
    for index, header in enumerate(headers):
        if index == subscribe_index:
            enriched_headers.extend(["Subscribe Date", "Subscribe Time (UTC)", "Subscribe Weekday"])
        else:
            enriched_headers.append(header)

    enriched_rows: list[list[str]] = []
    for row in rows:
        normalized_row = row + [""] * (len(headers) - len(row))
        date_text, time_text, weekday_text = parse_subscribe_date(normalized_row[subscribe_index])

        expanded_row: list[str] = []
        for index, value in enumerate(normalized_row):
            if index == subscribe_index:
                expanded_row.extend([date_text, time_text, weekday_text])
            else:
                expanded_row.append(value)

        enriched_rows.append(expanded_row)

    return enriched_headers, enriched_rows


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

        self.headers = headers
        self.all_rows = rows
        self.column_lookup = {name: index for index, name in enumerate(self.headers)}

        self.setWindowTitle("Meridian Subscribers")
        self.resize(1120, 700)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        top_panel = QFrame()
        top_panel.setObjectName("TopPanel")
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(14, 14, 14, 14)
        top_layout.setSpacing(10)

        title = QLabel("Meridian Subscriber Explorer")
        title.setObjectName("TitleLabel")
        top_layout.addWidget(title)

        subtitle = QLabel("Search, filter, and scan your subscriber CSV quickly")
        subtitle.setObjectName("SubTitleLabel")
        top_layout.addWidget(subtitle)

        controls = QHBoxLayout()
        controls.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by username or any visible value")
        controls.addWidget(self.search_input, 2)

        self.tier_filter = QComboBox()
        self.subtype_filter = QComboBox()
        self.founder_filter = QComboBox()

        self._populate_filter(self.tier_filter, "Current Tier", "All Tiers")
        self._populate_filter(self.subtype_filter, "Sub Type", "All Sub Types")
        self._populate_filter(self.founder_filter, "Founder", "All Founder States")

        controls.addWidget(self.tier_filter, 1)
        controls.addWidget(self.subtype_filter, 1)
        controls.addWidget(self.founder_filter, 1)
        top_layout.addLayout(controls)

        self.summary = QLabel()
        self.summary.setObjectName("SummaryLabel")
        top_layout.addWidget(self.summary)

        top_panel.setLayout(top_layout)
        layout.addWidget(top_panel)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.search_input.textChanged.connect(self.refresh_table)
        self.tier_filter.currentIndexChanged.connect(self.refresh_table)
        self.subtype_filter.currentIndexChanged.connect(self.refresh_table)
        self.founder_filter.currentIndexChanged.connect(self.refresh_table)

        self.refresh_table()

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def _populate_filter(self, combo: QComboBox, column_name: str, all_label: str) -> None:
        combo.clear()
        combo.addItem(all_label, "")

        column_index = self.column_lookup.get(column_name)
        if column_index is None:
            combo.setEnabled(False)
            return

        values = sorted({row[column_index] for row in self.all_rows if column_index < len(row) and row[column_index]})
        for value in values:
            combo.addItem(value, value)

    def _row_matches_filters(self, row: list[str], search_query: str) -> bool:
        tier_value = self.tier_filter.currentData()
        subtype_value = self.subtype_filter.currentData()
        founder_value = self.founder_filter.currentData()

        if search_query:
            haystack = " ".join(row).lower()
            if search_query not in haystack:
                return False

        if tier_value and row[self.column_lookup["Current Tier"]] != tier_value:
            return False
        if subtype_value and row[self.column_lookup["Sub Type"]] != subtype_value:
            return False
        if founder_value and row[self.column_lookup["Founder"]] != founder_value:
            return False

        return True

    def refresh_table(self) -> None:
        search_query = self.search_input.text().strip().lower()
        matching_rows = [row for row in self.all_rows if self._row_matches_filters(row, search_query)]

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(matching_rows))

        for row_index, row in enumerate(matching_rows):
            for column_index, value in enumerate(row):
                self.table.setItem(row_index, column_index, QTableWidgetItem(value))

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.summary.setText(f"Showing {len(matching_rows)} of {len(self.all_rows)} subscribers")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_palette(app)
    csv_headers, csv_rows = read_subscribers_csv("subscriber-list.csv")
    csv_headers, csv_rows = enrich_subscribe_date(csv_headers, csv_rows)
    window = MyWidget(csv_headers, csv_rows)
    window.show()

    sys.exit(app.exec())