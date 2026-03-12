"""
DtGUI Saved Timeline Plugin - Hook Implementations

This plugin adds a "Saved Timeline" menu that shows previously imported timelines
for quick re-access without reimporting.
"""

import DtGUI
import os
from functools import partial
from PyQt5.QtWidgets import QAction

from .saved_timeline import SavedTimelineManager
from QtDatabase import host as QtDatabase_Plugin


# Global manager instance
_saved_timeline_manager = None


def get_manager() -> SavedTimelineManager:
    """
    Get or create the SavedTimelineManager singleton instance.
    
    Returns:
        The global SavedTimelineManager instance
    """
    global _saved_timeline_manager
    if _saved_timeline_manager is None:
        _saved_timeline_manager = SavedTimelineManager()
    return _saved_timeline_manager


def open_timeline_directly(DtGUIObj, directory: str, timeline_name: str, column_names: list) -> None:
    """
    Open a saved timeline directly without reimporting.
    
    Sets up the database connection and triggers the timeline display.
    
    Args:
        DtGUIObj: The main DtGUI application object
        directory: Path to the case directory
        timeline_name: Name of the timeline table
        column_names: List of column names in the timeline
    """
    # Set up database connection
    DtGUIObj.database = QtDatabase_Plugin.QtDatabase(directory)
    DtGUIObj.database.connection.open()

    # Set case info
    DtGUIObj.case_name = os.path.basename(directory)
    DtGUIObj.case_directory = directory

    # Trigger timeline subwindow
    DtGUIObj.timeline_subwindow_trigger(timeline_name, column_names)

    # Save to timeline_columns for merge functionality
    DtGUIObj.timeline_columns[timeline_name] = column_names


@DtGUI.hookimpl
def init_menu(DtGUIObj):
    """
    Add Saved Timeline menu to the main application.
    
    Creates a menu showing all previously saved timelines grouped by case directory.
    Users can click on any saved timeline to reopen it without reimporting.
    
    Args:
        DtGUIObj: The main DtGUI application object
    """
    menubar = DtGUIObj.menuBar()
    manager = get_manager()

    # Create Saved Timeline menu
    saved_timeline_menu = menubar.addMenu('&Saved Timeline')

    # Get all saved timelines
    saved_timelines = manager.get_all_timelines()

    if saved_timelines:
        for directory in saved_timelines:
            # Create submenu for each case directory
            case_menu = saved_timeline_menu.addMenu(os.path.basename(directory))

            if "timelines" in saved_timelines[directory]:
                for timeline_name in saved_timelines[directory]["timelines"]:
                    column_names = saved_timelines[directory]["timelines"][timeline_name]

                    timeline_act = QAction(f'Open timeline {timeline_name}', DtGUIObj)
                    timeline_act.setStatusTip('Show saved timeline')
                    timeline_act.triggered.connect(
                        partial(open_timeline_directly, DtGUIObj, directory, timeline_name, column_names)
                    )
                    case_menu.addAction(timeline_act)
    else:
        no_saved_act = QAction('No Saved timelines', DtGUIObj)
        no_saved_act.setEnabled(False)
        saved_timeline_menu.addAction(no_saved_act)


def save_imported_timeline(case_directory: str, table_name: str, column_names: list) -> None:
    """
    Save an imported timeline to the JSON file.
    
    This should be called after importing a timeline to persist it 
    for quick access later.
    
    Args:
        case_directory: Path to the case directory
        table_name: Name of the timeline table
        column_names: List of column names in the timeline
    """
    manager = get_manager()
    manager.save_timeline(case_directory, table_name, column_names)
