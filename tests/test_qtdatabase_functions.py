"""
Unit Tests for Refactored QtDatabase Functions

Tests the extracted utility functions from QtDatabase plugin.
"""

import pytest
import os
import sys

# Add the plugin to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'plugins', 'QtDatabase'))

from QtDatabase.lib import build_column_string, build_placeholders


class TestBuildColumnString:
    """Test suite for build_column_string function"""
    
    def test_basic_columns(self):
        """Test basic column string building"""
        result = build_column_string(['name', 'age', 'city'])
        assert result == "name, age, city"
    
    def test_single_column(self):
        """Test single column"""
        result = build_column_string(['name'])
        assert result == "name"
    
    def test_with_type(self):
        """Test column string with TEXT type"""
        result = build_column_string(['name', 'age'], with_type=True)
        assert result == "name TEXT, age TEXT"
    
    def test_empty_list(self):
        """Test empty column list"""
        result = build_column_string([])
        assert result == ""


class TestBuildPlaceholders:
    """Test suite for build_placeholders function"""
    
    def test_single_placeholder(self):
        """Test single placeholder"""
        assert build_placeholders(1) == "?"
    
    def test_multiple_placeholders(self):
        """Test multiple placeholders"""
        assert build_placeholders(3) == "?, ?, ?"
    
    def test_zero_placeholders(self):
        """Test zero placeholders"""
        assert build_placeholders(0) == ""
    
    def test_many_placeholders(self):
        """Test many placeholders"""
        result = build_placeholders(5)
        assert result == "?, ?, ?, ?, ?"
        assert result.count('?') == 5
