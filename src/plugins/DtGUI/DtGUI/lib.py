import DtGUI, os, re
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    qApp,
    QApplication,
    QFileDialog,
    QMessageBox,
    QMdiArea
)
from PyQt5 import QtGui
from QtDatabase import host as QtDatabase_Plugin
from TimelineSubWindow import host as TimelineSubWindow_Plugin
from MergeTimelineSubWindow import host as MergeTimelineSubWindow_Plugin

@DtGUI.hookimpl
def init_ui(DtGUIObj):
    DtGUIObj.statusBar()
    # show main window
    DtGUIObj.setWindowIcon(QtGui.QIcon('../assets/drone.png'))
    DtGUIObj.setGeometry(50, 50, 800, 600)
    DtGUIObj.setWindowTitle(DtGUIObj.main_window_title)
    DtGUIObj.show()

# No menus in base app - all menus come from plugins:
# - DtGUI-FileMenu: File menu (Select Directory, Import, Exit)
# - DtGUI-TimelineMenu: Timeline menu (Merge, Show Merged)
# - DtGUI-SavedTimeline: Saved Timeline menu

@DtGUI.hookimpl
def timeline_subwindow_trigger(DtGUIObj, table_name, column_names):
    # define and show timeline sub window
    subwindow = TimelineSubWindow_Plugin.TimelineSubWindow(table_name, column_names, DtGUIObj.database.connection)
    DtGUIObj.mdi.addSubWindow(subwindow)
    subwindow.show_ui()

@DtGUI.hookimpl
def merge_window_trigger(DtGUIObj):
    # define and show merge timeline config sub window
    subwindow = MergeTimelineSubWindow_Plugin.MergeTimelineSubWindow(DtGUIObj.timeline_columns, DtGUIObj.database, DtGUIObj.merged_timeline_table_name)
    DtGUIObj.mdi.addSubWindow(subwindow)
    subwindow.show_ui()

@DtGUI.hookimpl
def merged_timeline_window_trigger(DtGUIObj):
    if DtGUIObj.database is None:
        DtGUIObj.show_info_messagebox('Please select case directory, import timeline, and then merge timeline.')

    else:
        # define and show merged timeline sub window
        subwindow = TimelineSubWindow_Plugin.TimelineSubWindow(DtGUIObj.merged_timeline_table_name,
                                        ['timestamp', 'event'], DtGUIObj.database.connection)
        DtGUIObj.mdi.addSubWindow(subwindow)
        subwindow.show_ui()

@DtGUI.hookimpl
def show_info_messagebox(text):
    dlg = QMessageBox()
    dlg.setWindowTitle("DroneTimeline")
    dlg.setText(text)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setIcon(QMessageBox.Information)
    dlg.exec_()