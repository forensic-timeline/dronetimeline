"""
DtGUI File Menu Plugin - Hook Implementations

This plugin adds the File menu with:
- Select Case Directory
- Import Timeline
- Exit
"""

import DtGUI
import os
import re
from PyQt5.QtWidgets import QAction, QFileDialog, qApp

from QtDatabase import host as QtDatabase_Plugin


def sanitize_table_name(filename: str) -> str:
    """
    Convert a filename to a valid table name.
    
    Removes file extension and all non-alphanumeric characters.
    
    Args:
        filename: The original filename (can include path and extension)
    
    Returns:
        A sanitized alphanumeric string suitable for database table names
    
    Example:
        >>> sanitize_table_name("hasil-1.csv")
        'hasil1'
        >>> sanitize_table_name("/path/to/my_file.csv")
        'myfile'
    """
    # Get just the filename without path
    base_name = os.path.basename(filename)
    # Remove extension
    name_without_ext = os.path.splitext(base_name)[0]
    # Remove non-alphanumeric characters
    return re.sub(r'[\W_]+', '', name_without_ext)


def select_case_directory(DtGUIObj, directory: str) -> bool:
    """
    Set up the case directory and initialize database connection.
    
    Args:
        DtGUIObj: The main DtGUI application object
        directory: Path to the case directory
    
    Returns:
        True if directory was successfully set, False otherwise
    """
    if not directory:
        return False
    
    database_name = os.path.basename(directory)
    if not database_name:
        return False
    
    # Initialize database connection
    DtGUIObj.database = QtDatabase_Plugin.QtDatabase(os.path.join(directory, database_name))
    
    # Set case name and directory
    DtGUIObj.case_name = database_name
    DtGUIObj.case_directory = directory
    
    return True


def import_timeline(DtGUIObj, file_path: str) -> tuple:
    """
    Import a CSV timeline file into the database.
    
    Args:
        DtGUIObj: The main DtGUI application object
        file_path: Path to the CSV file to import
    
    Returns:
        Tuple of (table_name, column_names) if successful, (None, None) otherwise
    """
    if not file_path:
        return None, None
    
    # Sanitize table name
    table_name = sanitize_table_name(file_path)
    
    # Insert CSV into database
    column_names = DtGUIObj.database.insert_csv(table_name, file_path)
    
    # Save timeline columns for merge functionality
    DtGUIObj.timeline_columns[table_name] = column_names
    
    return table_name, column_names


@DtGUI.hookimpl
def init_menu(DtGUIObj):
    """
    Add File menu to the main application.
    
    Creates the File menu with the following actions:
    - Select Case Directory (Ctrl+N): Choose working directory
    - Import Timeline (Ctrl+I): Import a CSV timeline file
    - Exit (Ctrl+Q): Close the application
    
    Args:
        DtGUIObj: The main DtGUI application object
    """
    menubar = DtGUIObj.menuBar()
    file_menu = menubar.addMenu('&File')

    # ================== Select Case Directory ==================
    newcase_act = QAction('&Select Case Directory', DtGUIObj)
    newcase_act.setShortcut('Ctrl+N')
    newcase_act.setStatusTip('Select case directory')

    def on_select_directory():
        """Handle Select Case Directory menu action."""
        directory = QFileDialog.getExistingDirectory(DtGUIObj, "Select Directory")
        if select_case_directory(DtGUIObj, directory):
            message = f'Case directory is selected: {directory}'
            DtGUIObj.show_info_messagebox(message)

    newcase_act.triggered.connect(on_select_directory)
    file_menu.addAction(newcase_act)

    # ================== Import Timeline ==================
    import_act = QAction('&Import Timeline', DtGUIObj)
    import_act.setShortcut('Ctrl+I')
    import_act.setStatusTip('Import timeline')

    def on_import_timeline():
        """Handle Import Timeline menu action."""
        if DtGUIObj.case_name == '':
            DtGUIObj.show_info_messagebox("Please select case directory before importing a timeline.")
            return
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(DtGUIObj, "Open file", "", "All Files (*)", options=options)
        
        if file_name:
            table_name, column_names = import_timeline(DtGUIObj, file_name)
            if table_name:
                DtGUIObj.timeline_subwindow_trigger(table_name, column_names)
                message = f'Timeline is imported successfully: {table_name}.'
                DtGUIObj.show_info_messagebox(message)

    import_act.triggered.connect(on_import_timeline)
    file_menu.addAction(import_act)

    # ================== Exit ==================
    exit_act = QAction('&Exit', DtGUIObj)
    exit_act.setShortcut('Ctrl+Q')
    exit_act.setStatusTip('Exit application')
    exit_act.triggered.connect(qApp.quit)
    file_menu.addAction(exit_act)
