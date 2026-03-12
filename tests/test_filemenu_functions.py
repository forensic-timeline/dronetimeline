"""
Unit Tests for Refactored FileMenu Functions

Tests the extracted utility functions for testability.
"""

import pytest
import os
import sys

# Add the plugin to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'plugins', 'DtGUI-FileMenu'))

from DtGUI_FileMenu.plugin_hooks import sanitize_table_name


class TestSanitizeTableName:
    """Test suite for sanitize_table_name function"""
    
    def test_basic_filename(self):
        """Test basic filename sanitization"""
        assert sanitize_table_name("hasil1.csv") == "hasil1"
    
    def test_filename_with_hyphen(self):
        """Test filename with hyphens"""
        assert sanitize_table_name("hasil-1.csv") == "hasil1"
    
    def test_filename_with_underscore(self):
        """Test filename with underscores"""
        assert sanitize_table_name("hasil_1.csv") == "hasil1"
    
    def test_filename_with_spaces(self):
        """Test filename with spaces"""
        assert sanitize_table_name("hasil 1.csv") == "hasil1"
    
    def test_filename_with_path(self):
        """Test full path with filename"""
        assert sanitize_table_name("/path/to/my_file.csv") == "myfile"
    
    def test_windows_path(self):
        """Test Windows-style path"""
        assert sanitize_table_name("C:\\Users\\test\\file-name.csv") == "filename"
    
    def test_multiple_extensions(self):
        """Test filename with multiple dots"""
        assert sanitize_table_name("data.backup.csv") == "databackup"
    
    def test_special_characters(self):
        """Test filename with special characters"""
        assert sanitize_table_name("data@#$%.csv") == "data"
    
    def test_unicode_characters(self):
        """Test filename with unicode characters"""
        # Unicode letters are preserved by \W regex
        assert sanitize_table_name("données.csv") == "données"
    
    def test_empty_after_sanitize(self):
        """Test filename that becomes empty after sanitization"""
        # Should return empty string
        result = sanitize_table_name("@#$%.csv")
        assert result == ""
