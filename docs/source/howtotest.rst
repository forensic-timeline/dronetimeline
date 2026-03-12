How to run tests
================

DroneTimeline includes unit tests to verify the functionality of its plugins.

.. note:: Make sure all plugins are installed before running tests.

1. Navigate to the project root directory::

       cd dronetimeline

2. Run all tests::

       python -m pytest tests/ -v

3. Run a specific test file::

       python -m pytest tests/test_filemenu_functions.py -v

4. Run a specific test function::

       python -m pytest tests/test_filemenu_functions.py::TestSanitizeTableName::test_basic_filename -v

Test Files
----------

- ``tests/test_filemenu_functions.py``: Tests for the sanitize_table_name function.
- ``tests/test_qtdatabase_functions.py``: Tests for build_column_string and build_placeholders functions.
- ``tests/test_qtdatabase.py``: Integration tests for QtDatabase operations.
- ``tests/test_saved_timeline.py``: Tests for SavedTimelineManager JSON operations.
- ``tests/test_plugin_hooks.py``: Tests for plugin hook registration and functionality.
