Installation
============

To install DroneTimeline, follow these steps:

.. note:: Make sure you have Python 3.10 or higher installed.

1. Clone the repository.

   Clone the DroneTimeline repository from GitHub::

       git clone https://github.com/studiawan/dronetimeline.git

2. Navigate to the project directory::

       cd dronetimeline

3. Install the core plugins.

   Install each plugin in development mode::

       pip install --editable src/plugins/DtGUI
       pip install --editable src/plugins/QtDatabase
       pip install --editable src/plugins/TimelineSubWindow
       pip install --editable src/plugins/MergeTimelineSubWindow

4. Install menu plugins::

       pip install --editable src/plugins/DtGUI-FileMenu
       pip install --editable src/plugins/DtGUI-TimelineMenu

5. Install optional plugins::

       pip install --editable src/plugins/DtGUI-SavedTimeline
       pip install --editable src/plugins/DtGUI-EntityRecognition

Dependencies
------------

The following Python packages are required:

- PyQt5
- pluggy
- spacy (for Entity Recognition plugin)
