"""
QtDatabase Plugin - Database Operations

This module provides database operations for the DroneTimeline application:
- create_table: Create a new database table
- insert_data: Insert a row into a table
- insert_csv: Import CSV file into database
- insert_into_merged_timeline: Merge multiple timelines into one
"""

import QtDatabase
import os
import csv
from typing import List, Dict, Any
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def build_column_string(column_names: List[str], with_type: bool = False) -> str:
    """
    Build a comma-separated column string for SQL queries.
    
    Args:
        column_names: List of column names
        with_type: If True, append ' TEXT' to each column name
    
    Returns:
        Comma-separated string of column names
    
    Example:
        >>> build_column_string(['name', 'age'], with_type=True)
        'name TEXT, age TEXT'
        >>> build_column_string(['name', 'age'])
        'name, age'
    """
    type_suffix = ' TEXT' if with_type else ''
    return ', '.join(f"{col}{type_suffix}" for col in column_names)


def build_placeholders(count: int) -> str:
    """
    Build placeholder string for parameterized SQL queries.
    
    Args:
        count: Number of placeholders needed
    
    Returns:
        Comma-separated string of question marks
    
    Example:
        >>> build_placeholders(3)
        '?, ?, ?'
    """
    return ', '.join('?' for _ in range(count))


@QtDatabase.hookimpl
def create_table(QtDatabaseObj, table_name: str, column_names: List[str]) -> None:
    """
    Create a new database table.
    
    Drops existing table with the same name to prevent duplicate data on reimport.
    
    Args:
        QtDatabaseObj: The QtDatabase instance
        table_name: Name of the table to create
        column_names: List of column names (all columns are TEXT type)
    """
    if not QtDatabaseObj.connection.open():
        print("Database Error: %s" % QtDatabaseObj.connection.lastError().databaseText())
    
    query = QSqlQuery()
    
    # Drop table if exists to prevent duplicate data on reimport
    drop_query_string = f"DROP TABLE IF EXISTS {table_name}"
    query.exec(drop_query_string)
    
    # Build CREATE TABLE query
    column_string = build_column_string(column_names, with_type=True)
    query_string = f"CREATE TABLE IF NOT EXISTS {table_name}" \
                    f" (id INTEGER PRIMARY KEY AUTOINCREMENT, {column_string})"
    
    query.exec(query_string)


@QtDatabase.hookimpl
def insert_data(table_name: str, column_names: List[str], row: List[str]) -> None:
    """
    Insert a single row of data into a table.
    
    Uses parameterized queries to prevent SQL injection.
    
    Args:
        table_name: Name of the table
        column_names: List of column names
        row: List of values to insert (must match column_names length)
    """
    insert_query = QSqlQuery()
    
    # Build INSERT query with placeholders
    columns = build_column_string(column_names)
    placeholders = build_placeholders(len(column_names))
    query_string = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    insert_query.prepare(query_string)
    
    # Bind values
    for value in row:
        insert_query.addBindValue(value)
    
    insert_query.exec()


@QtDatabase.hookimpl
def insert_csv(QtDatabaseObj, table_name: str, csv_path: str) -> List[str]:
    """
    Import a CSV file into the database.
    
    The first row of the CSV is used as column names.
    Creates a new table and inserts all data rows.
    
    Args:
        QtDatabaseObj: The QtDatabase instance
        table_name: Name of the table to create
        csv_path: Path to the CSV file
    
    Returns:
        List of column names from the CSV header
    """
    with open(csv_path) as f:
        csv_reader = csv.reader(f, delimiter=',')

        line_count = 0
        column_names = []
        for row in csv_reader:
            if line_count == 0:
                # First row is header - get column names and create table
                column_names = row
                QtDatabaseObj.create_table(table_name, column_names)
                line_count += 1
            else:
                # Data rows - insert into table
                QtDatabaseObj.insert_data(table_name, column_names, row)

    return column_names


@QtDatabase.hookimpl
def insert_into_merged_timeline(QtDatabaseObj, selected_columns: Dict[str, Dict[str, str]], 
                                 merged_timeline_table: str) -> None:
    """
    Merge multiple timelines into a single merged timeline table.
    
    Selects timestamp and event columns from each source timeline
    and combines them into one table with source tracking.
    
    Args:
        QtDatabaseObj: The QtDatabase instance
        selected_columns: Dictionary mapping timeline names to their selected columns
                         Format: {timeline_name: {'timestamp': col_name, 'event': col_name}}
        merged_timeline_table: Name of the merged timeline table to create
    """
    # Create merged timeline table with standard columns
    merged_columns = ['timestamp', 'event', 'source']
    QtDatabaseObj.create_table(merged_timeline_table, merged_columns)

    # Process each source timeline
    for timeline_name, column_names in selected_columns.items():
        # Sort columns to ensure order: [timestamp, event]
        column_sorted = []
        for column_type, column_name in column_names.items():
            if column_type == 'timestamp':
                if len(column_sorted) > 1:
                    column_sorted.insert(0, column_name)
                else:
                    column_sorted.append(column_name)
            elif column_type == 'event':
                column_sorted.append(column_name)

        # Build and execute SELECT query
        column_string = build_column_string(column_sorted)
        query_string = f"SELECT {column_string} FROM {timeline_name}"
        
        select_query = QSqlQuery()
        select_query.exec(query_string)

        # Insert each row into merged timeline
        while select_query.next():
            row = [
                select_query.value(column_sorted[0]),  # timestamp
                select_query.value(column_sorted[1]),  # event
                timeline_name                          # source
            ]
            QtDatabaseObj.insert_data(merged_timeline_table, merged_columns, row)