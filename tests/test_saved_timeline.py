"""
Unit Tests for SavedTimelineManager

Tests the JSON read/write operations for saved timelines.
"""

import pytest
import os
import json
import tempfile
import shutil

# Add the plugin to the path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'plugins', 'DtGUI-SavedTimeline'))

from DtGUI_SavedTimeline.saved_timeline import SavedTimelineManager


class TestSavedTimelineManager:
    """Test suite for SavedTimelineManager"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def manager(self, temp_dir):
        """Create a SavedTimelineManager with a temp JSON file"""
        json_path = os.path.join(temp_dir, 'timelines.json')
        return SavedTimelineManager(json_path)
    
    def test_init_creates_empty_file(self, temp_dir):
        """Test that initialization creates an empty JSON file if it doesn't exist"""
        json_path = os.path.join(temp_dir, 'test_timelines.json')
        manager = SavedTimelineManager(json_path)
        
        assert os.path.exists(json_path)
        assert manager.get_all_timelines() == {}
    
    def test_save_timeline(self, manager):
        """Test saving a timeline entry"""
        case_dir = '/path/to/case'
        table_name = 'hasil1'
        column_names = ['timestamp', 'message', 'short']
        
        manager.save_timeline(case_dir, table_name, column_names)
        
        timelines = manager.get_all_timelines()
        assert case_dir in timelines
        assert 'timelines' in timelines[case_dir]
        assert table_name in timelines[case_dir]['timelines']
        assert timelines[case_dir]['timelines'][table_name] == column_names
    
    def test_save_multiple_timelines(self, manager):
        """Test saving multiple timelines to the same case"""
        case_dir = '/path/to/case'
        
        manager.save_timeline(case_dir, 'timeline1', ['col1', 'col2'])
        manager.save_timeline(case_dir, 'timeline2', ['col3', 'col4'])
        
        timelines = manager.get_all_timelines()
        assert len(timelines[case_dir]['timelines']) == 2
        assert 'timeline1' in timelines[case_dir]['timelines']
        assert 'timeline2' in timelines[case_dir]['timelines']
    
    def test_save_timelines_different_cases(self, manager):
        """Test saving timelines to different cases"""
        manager.save_timeline('/case1', 'timeline1', ['col1'])
        manager.save_timeline('/case2', 'timeline2', ['col2'])
        
        timelines = manager.get_all_timelines()
        assert len(timelines) == 2
        assert '/case1' in timelines
        assert '/case2' in timelines
    
    def test_does_not_duplicate_timeline(self, manager):
        """Test that saving the same timeline twice doesn't create duplicates"""
        case_dir = '/path/to/case'
        table_name = 'timeline1'
        
        manager.save_timeline(case_dir, table_name, ['col1'])
        manager.save_timeline(case_dir, table_name, ['col2'])  # Different columns, same name
        
        timelines = manager.get_all_timelines()
        # Should keep the first one (not overwrite)
        assert timelines[case_dir]['timelines'][table_name] == ['col1']
    
    def test_persistence(self, temp_dir):
        """Test that saved timelines persist across manager instances"""
        json_path = os.path.join(temp_dir, 'persist_test.json')
        
        # Save with first instance
        manager1 = SavedTimelineManager(json_path)
        manager1.save_timeline('/case', 'timeline', ['col1', 'col2'])
        
        # Load with second instance
        manager2 = SavedTimelineManager(json_path)
        timelines = manager2.get_all_timelines()
        
        assert '/case' in timelines
        assert 'timeline' in timelines['/case']['timelines']
