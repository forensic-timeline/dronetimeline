"""
DtGUI Timeline Menu Plugin - Hook Implementations

This plugin adds the Timeline menu with:
- Merge Timelines: Combine multiple imported timelines
- Show Merged Timeline: Display the merged result
"""

import DtGUI
from PyQt5.QtWidgets import QAction


@DtGUI.hookimpl
def init_menu(DtGUIObj):
    """
    Add Timeline menu to the main application.
    
    Creates the Timeline menu with the following actions:
    - Merge Timelines (Ctrl+M): Open merge configuration window
    - Show Merged Timeline (Ctrl+H): Display merged timeline view
    
    Args:
        DtGUIObj: The main DtGUI application object
    """
    menubar = DtGUIObj.menuBar()
    timeline_menu = menubar.addMenu('&Timeline')

    # ================== Merge Timeline ==================
    merge_act = QAction('&Merge Timelines', DtGUIObj)
    merge_act.setShortcut('Ctrl+M')
    merge_act.setStatusTip('Merge timelines')
    merge_act.triggered.connect(DtGUIObj.merge_window_trigger)
    timeline_menu.addAction(merge_act)

    # ================== Show Merged Timeline ==================
    show_merged_timeline_act = QAction('S&how Merged Timeline', DtGUIObj)
    show_merged_timeline_act.setShortcut('Ctrl+H')
    show_merged_timeline_act.setStatusTip('Show merged timeline')
    show_merged_timeline_act.triggered.connect(DtGUIObj.merged_timeline_window_trigger)
    timeline_menu.addAction(show_merged_timeline_act)
