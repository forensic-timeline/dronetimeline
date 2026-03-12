"""
CSV Import with Entity Recognition - Sub Window

Provides a progress bar while importing CSV files and applying
entity recognition to annotate text columns.
"""

import os
import csv
import time
from PyQt5.QtWidgets import QMdiSubWindow, QProgressBar
from PyQt5.QtCore import pyqtSignal
from .entity_recognition import EntityRecognition


class CSVImportSubWindow(QMdiSubWindow):
    """
    Sub window for importing CSV files with entity recognition.
    
    Shows a progress bar during import and applies entity recognition
    to text columns ('event', 'short', 'message').
    
    Signals:
        import_complete: Emitted when import finishes (table_name, column_names)
    """

    import_complete = pyqtSignal(str, list)

    def __init__(self, csv_file: str, table_name: str, column_names: list,
                 database_path: str, parent_gui=None):
        """
        Initialize the CSV Import sub window.
        
        Args:
            csv_file: Path to the CSV file to import
            table_name: Database table name for this timeline
            column_names: List of column names from the CSV header
            database_path: Path to the database file
            parent_gui: The main DtGUI application object (for signal connection)
        """
        super().__init__()
        self.table_name = table_name
        self.csv_file = csv_file
        self.column_names = column_names
        self.database_path = database_path
        self.parent_gui = parent_gui
        self.progress = None
        self.completed = 0

        if parent_gui:
            self.import_complete.connect(parent_gui.timeline_subwindow_trigger)

    def insert_csv_to_db(self) -> None:
        """
        Import CSV data with entity recognition and insert into database.
        
        Reads the CSV file, applies entity recognition to event/message columns,
        writes IOB format output, and inserts annotated data into the SQLite database.
        """
        import sqlite3

        entity_recognition = EntityRecognition()

        # Count total lines for progress bar
        with open(self.csv_file) as f:
            total_lines = sum(1 for _ in f) + 1

        # Open IOB output file
        iob_file = open(self.table_name + '_IOB.txt', 'w')

        # Connect to database
        con = sqlite3.connect(f"{os.path.basename(self.database_path)}.db")
        cur = con.cursor()

        # Check for existing data
        try:
            cur.execute(f"SELECT MAX(id) FROM {self.table_name}")
            row = cur.fetchone()[0]
            last_inserted_id = int(row) if row else 0
        except Exception:
            last_inserted_id = 0

        datas = []

        with open(self.csv_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)  # Skip header

            # Skip already-inserted rows
            for _ in range(last_inserted_id):
                next(csv_reader)
                self.completed += 1 / total_lines
                self.progress.setValue(int(self.completed * 100))

            # Find relevant column indices
            index_message = self._find_column_index('message')
            index_event = self._find_column_index('event') or self._find_column_index('short')

            for row in csv_reader:
                doc = None
                entities = []

                # Apply entity recognition
                if index_event is not None:
                    row[index_event], doc, entities = entity_recognition.find_entity(row[index_event])
                if index_message is not None:
                    row[index_message], doc, entities = entity_recognition.find_entity(row[index_message])

                datas.append(row)

                # Write IOB format
                if doc and entities:
                    iob_result = entity_recognition.iob_format(doc, entities)
                    for tag, token in iob_result:
                        iob_file.write(f"{tag} {token}\n")
                    iob_file.write('\n')

                self.completed += 1 / total_lines
                self.progress.setValue(int(self.completed * 100))

        iob_file.close()

        # Build and execute bulk INSERT
        columns = ', '.join(self.column_names)
        placeholders = ', '.join('?' for _ in self.column_names)
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        self.progress.setValue(95)
        cur.executemany(query, datas)
        con.commit()
        cur.close()
        self.progress.setValue(100)

        # Notify main thread
        self.import_complete.emit(self.table_name, self.column_names)

    def _find_column_index(self, column_name: str):
        """
        Find the index of a column name in the column list.
        
        Args:
            column_name: Column name to search for
        
        Returns:
            Column index if found, None otherwise
        """
        return self.column_names.index(column_name) if column_name in self.column_names else None

    def show_ui(self) -> None:
        """Display the import progress sub window."""
        subwindow_title = f"Reading Forensics timeline: {self.table_name}"
        self.setWindowTitle(subwindow_title)
        self.setGeometry(60, 60, 600, 400)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.resize(300, 100)
        self.show()
