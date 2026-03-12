"""
Unit Tests for Plugin Hooks

Tests that plugins are properly registered and hooks work correctly.
"""

import pytest
import pluggy

# Add plugins to path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'plugins', 'DtGUI'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'plugins', 'DtGUI-SavedTimeline'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'plugins', 'QtDatabase'))


class TestPluginRegistration:
    """Test suite for plugin registration and hooks"""
    
    def test_dtgui_hookspecs_defined(self):
        """Test that DtGUI hookspecs are properly defined"""
        from DtGUI import hookspecs
        
        # Check that hookspec marker exists
        assert hasattr(hookspecs, 'hookspec')
        
        # Check required hooks are defined
        assert hasattr(hookspecs, 'init_ui')
        assert hasattr(hookspecs, 'init_menu')
        assert hasattr(hookspecs, 'timeline_subwindow_trigger')
        assert hasattr(hookspecs, 'merge_window_trigger')
    
    def test_dtgui_plugin_manager_loads(self):
        """Test that DtGUI plugin manager initializes correctly"""
        from DtGUI import hookspecs, lib
        
        pm = pluggy.PluginManager("DtGUI")
        pm.add_hookspecs(hookspecs)
        pm.register(lib)
        
        # Verify hooks are registered
        assert pm.hook.init_ui is not None
        assert pm.hook.init_menu is not None
    
    def test_saved_timeline_hookimpl_exists(self):
        """Test that SavedTimeline plugin has proper hook implementations"""
        from DtGUI_SavedTimeline import plugin_hooks
        
        # Check that the init_menu hook is implemented
        assert hasattr(plugin_hooks, 'init_menu')
        
        # Check hook has the hookimpl marker
        func = plugin_hooks.init_menu
        assert hasattr(func, 'DtGUI_impl')
    
    def test_qtdatabase_hookspecs_defined(self):
        """Test that QtDatabase hookspecs are properly defined"""
        from QtDatabase import hookspecs
        
        assert hasattr(hookspecs, 'create_table')
        assert hasattr(hookspecs, 'insert_data')
        assert hasattr(hookspecs, 'insert_csv')
    
    def test_qtdatabase_plugin_manager_loads(self):
        """Test that QtDatabase plugin manager initializes correctly"""
        from QtDatabase import hookspecs, lib
        
        pm = pluggy.PluginManager("QtDatabase")
        pm.add_hookspecs(hookspecs)
        pm.register(lib)
        
        assert pm.hook.create_table is not None
        assert pm.hook.insert_data is not None


class TestSavedTimelinePlugin:
    """Test SavedTimeline plugin specific functionality"""
    
    def test_get_manager_singleton(self):
        """Test that get_manager returns a manager instance"""
        from DtGUI_SavedTimeline.plugin_hooks import get_manager
        
        manager1 = get_manager()
        manager2 = get_manager()
        
        # Should return the same instance
        assert manager1 is manager2
    
    def test_save_imported_timeline_function(self):
        """Test the save_imported_timeline helper function"""
        import tempfile
        import shutil
        from DtGUI_SavedTimeline.plugin_hooks import save_imported_timeline, get_manager
        from DtGUI_SavedTimeline.saved_timeline import SavedTimelineManager
        
        # Use temp file for testing
        temp_dir = tempfile.mkdtemp()
        try:
            json_path = os.path.join(temp_dir, 'test_timelines.json')
            
            # Create a fresh manager with temp path
            from DtGUI_SavedTimeline import plugin_hooks
            plugin_hooks._saved_timeline_manager = SavedTimelineManager(json_path)
            
            save_imported_timeline('/test/case', 'test_table', ['col1', 'col2'])
            
            manager = get_manager()
            timelines = manager.get_all_timelines()
            
            assert '/test/case' in timelines
        finally:
            shutil.rmtree(temp_dir)
