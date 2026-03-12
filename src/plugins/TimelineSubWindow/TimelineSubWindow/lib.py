"""
TimelineSubWindow Plugin - Hook Implementations

Displays timeline data in a table view with search filtering.
Supports HTML rendering for entity-annotated text (highlighted entities).
"""

import TimelineSubWindow
from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QTableView,
    QLabel,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QApplication,
    QStyle
)
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtGui import QTextDocument, QAbstractTextDocumentLayout, QPalette
from PyQt5.QtCore import QSize, Qt, QRectF
from PyQt5 import QtGui


class HTMLDelegate(QStyledItemDelegate):
    """
    Custom delegate that renders HTML content in QTableView cells.
    
    This enables entity recognition highlights (yellow background,
    bold text with subscript labels) to be displayed properly.
    """

    def paint(self, painter, option, index):
        """Paint the cell with HTML rendering."""
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        painter.save()

        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())

        options.text = ""
        style = QApplication.style()
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)

        painter.translate(options.rect.left(), options.rect.top())
        clip = QRectF(0, 0, float(options.rect.width()), float(options.rect.height()))
        doc.drawContents(painter, clip)

        painter.restore()

    def sizeHint(self, option, index):
        """Calculate the size hint based on HTML content."""
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width() if options.rect.width() > 0 else 300)

        return QSize(int(doc.idealWidth()), int(doc.size().height()))


@TimelineSubWindow.hookimpl
def show_ui(TimeLineSubWindowObj):
    # set title and geometry
    subwindow_title = f"{'Drone Timeline: '}{TimeLineSubWindowObj.table_name}"
    TimeLineSubWindowObj.setWindowIcon(QtGui.QIcon('../assets/drone.png'))
    TimeLineSubWindowObj.setWindowTitle(subwindow_title)
    TimeLineSubWindowObj.setGeometry(60, 60, 600, 400)

    # construct the top level widget and layout
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # set table from database
    TimeLineSubWindowObj.table_model = QSqlTableModel(db=TimeLineSubWindowObj.db_connection)
    TimeLineSubWindowObj.table_model.setTable(TimeLineSubWindowObj.table_name)
    TimeLineSubWindowObj.table_model.select()

    # define search widget
    search_label = QLabel()
    search_label.setText('Search event or message:')
    search = QLineEdit()

    # define table widget
    table_label = QLabel()
    table_label.setText('Merged timeline:')
    table_widget = QTableView()
    table_widget.setModel(TimeLineSubWindowObj.table_model)

    # Add HTML delegate to render entity highlights
    html_delegate = HTMLDelegate()
    table_widget.setItemDelegate(html_delegate)

    # search event
    search.textChanged.connect(TimeLineSubWindowObj.update_filter)

    # add widget to layout
    layout.addWidget(search_label)
    layout.addWidget(search)
    layout.addWidget(table_label)
    layout.addWidget(table_widget)
    widget.setLayout(layout)

    # set widget to subwindow
    TimeLineSubWindowObj.setWidget(widget)
    TimeLineSubWindowObj.show()

@TimelineSubWindow.hookimpl
def get_column_intersection(TimeLineSubWindowObj):
    # get column event or message, get the first one found
    intersection = set(TimeLineSubWindowObj.column_names).intersection(set(TimeLineSubWindowObj.event_columns))
    intersection = list(intersection)
    event_column = intersection[0]

    return event_column

@TimelineSubWindow.hookimpl
def update_filter(TimeLineSubWindowObj, s):
    percent = '%'
    filter_str = f"{TimeLineSubWindowObj.event_column}{' LIKE '}\"{percent}{s}{percent}\""
    TimeLineSubWindowObj.table_model.setFilter(filter_str)