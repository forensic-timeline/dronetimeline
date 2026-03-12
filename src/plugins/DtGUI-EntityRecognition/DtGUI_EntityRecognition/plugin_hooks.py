"""
DtGUI Entity Recognition Plugin - Hook Implementations

This plugin adds an Entity Recognition menu that allows the user
to apply rule-based entity detection to the currently open merged timeline.
Entities are highlighted with yellow background in the event column.
"""

import DtGUI
from PyQt5.QtWidgets import QAction
from PyQt5.QtSql import QSqlQuery

from .entity_recognition import EntityRecognition


def apply_entity_recognition_to_table(database, table_name: str, text_column: str = 'event') -> int:
    """
    Apply entity recognition to all rows in a database table.

    Reads each row's text column, runs entity recognition on it,
    and updates the column with the HTML-annotated result.

    Args:
        database: QtDatabase instance with an open connection
        table_name: Name of the table to process
        text_column: Column name containing text to annotate

    Returns:
        Number of rows processed
    """
    entity_recognition = EntityRecognition()

    if not database.connection.open():
        print("Database Error: %s" % database.connection.lastError().databaseText())
        return 0

    # Read all rows
    select_query = QSqlQuery()
    select_query.exec(f"SELECT id, {text_column} FROM {table_name}")

    updates = []
    while select_query.next():
        row_id = select_query.value(0)
        original_text = select_query.value(1)

        if original_text:
            text = str(original_text)
            # Skip rows that are already annotated
            if 'background-color:yellow' in text:
                continue
            annotated_text, doc, entities = entity_recognition.find_entity(text)
            if entities:
                updates.append((annotated_text, row_id))

    # Apply updates
    for annotated_text, row_id in updates:
        update_query = QSqlQuery()
        update_query.prepare(f"UPDATE {table_name} SET {text_column} = ? WHERE id = ?")
        update_query.addBindValue(annotated_text)
        update_query.addBindValue(row_id)
        update_query.exec()

    return len(updates)


@DtGUI.hookimpl
def init_menu(DtGUIObj):
    """
    Add Entity Recognition menu to the main application.

    Creates a menu with "Apply to Merged Timeline" action that runs
    entity recognition on the merged timeline's event column.

    Args:
        DtGUIObj: The main DtGUI application object
    """
    menubar = DtGUIObj.menuBar()
    entity_menu = menubar.addMenu('&Entity Recognition')

    apply_act = QAction('&Apply to Merged Timeline', DtGUIObj)
    apply_act.setShortcut('Ctrl+E')
    apply_act.setStatusTip('Apply entity recognition to merged timeline')

    def on_apply_entity_recognition():
        """Handle Apply Entity Recognition menu action."""
        if DtGUIObj.database is None:
            DtGUIObj.show_info_messagebox(
                "Please select a case directory, import timelines, and merge them first."
            )
            return

        # Apply entity recognition to the merged timeline
        count = apply_entity_recognition_to_table(
            DtGUIObj.database,
            DtGUIObj.merged_timeline_table_name,
            text_column='event'
        )

        if count > 0:
            message = f'Entity recognition applied to {count} rows in merged timeline.'
            DtGUIObj.show_info_messagebox(message)

            # Refresh the merged timeline view
            DtGUIObj.merged_timeline_window_trigger()
        else:
            DtGUIObj.show_info_messagebox(
                'No new entities found. The timeline may already have entity recognition applied, '
                'or no entities were detected.'
            )

    apply_act.triggered.connect(on_apply_entity_recognition)
    entity_menu.addAction(apply_act)
