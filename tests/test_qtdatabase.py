"""
Unit Tests for QtDatabase Plugin

Tests database create table and insert data operations.
"""

import pytest
import os
import tempfile
import shutil

# Add the plugin to the path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'plugins', 'QtDatabase'))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from QtDatabase import host as QtDatabase_Plugin


# Initialize QApplication for PyQt tests
@pytest.fixture(scope='session')
def app():
    """Create QApplication instance for the test session"""
    app = QApplication([])
    yield app


class TestQtDatabase:
    """Test suite for QtDatabase plugin"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test database"""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def database(self, temp_dir, app):
        """Create a QtDatabase instance with a temp database"""
        db_path = os.path.join(temp_dir, 'test_db')
        db = QtDatabase_Plugin.QtDatabase(db_path)
        yield db
        db.connection.close()
    
    def test_database_creation(self, database):
        """Test that database is created successfully"""
        assert database.connection is not None
        assert database.database_name.endswith('.db')
    
    def test_create_table(self, database):
        """Test creating a table"""
        table_name = 'test_table'
        column_names = ['col1', 'col2', 'col3']
        
        database.create_table(table_name, column_names)
        
        # Verify table exists
        query = QSqlQuery()
        query.exec(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        assert query.next() is True
    
    def test_insert_data(self, database):
        """Test inserting data into a table"""
        table_name = 'insert_test'
        column_names = ['name', 'value']
        
        database.create_table(table_name, column_names)
        database.insert_data(table_name, column_names, ['test_name', 'test_value'])
        
        # Verify data was inserted
        query = QSqlQuery()
        query.exec(f"SELECT * FROM {table_name}")
        assert query.next() is True
        assert query.value(1) == 'test_name'  # id is column 0
        assert query.value(2) == 'test_value'
    
    def test_table_replacement_on_reimport(self, database):
        """Test that reimporting drops and recreates the table"""
        table_name = 'reimport_test'
        column_names = ['data']
        
        # First import
        database.create_table(table_name, column_names)
        database.insert_data(table_name, column_names, ['first'])
        
        # Second import (should replace)
        database.create_table(table_name, column_names)
        database.insert_data(table_name, column_names, ['second'])
        
        # Verify only one row exists
        query = QSqlQuery()
        query.exec(f"SELECT COUNT(*) FROM {table_name}")
        query.next()
        count = query.value(0)
        assert count == 1
    
    def test_insert_csv(self, database, temp_dir):
        """Test importing a CSV file"""
        # Create a test CSV
        csv_path = os.path.join(temp_dir, 'test.csv')
        with open(csv_path, 'w') as f:
            f.write('name,age,city\n')
            f.write('Alice,30,NYC\n')
            f.write('Bob,25,LA\n')
        
        table_name = 'csv_test'
        column_names = database.insert_csv(table_name, csv_path)
        
        assert column_names == ['name', 'age', 'city']
        
        # Verify data was inserted
        query = QSqlQuery()
        query.exec(f"SELECT COUNT(*) FROM {table_name}")
        query.next()
        assert query.value(0) == 2  # Two data rows
