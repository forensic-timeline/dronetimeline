How to run
==========

To run DroneTimeline, follow these steps:

.. note:: Make sure all plugins are installed before running.

1. Navigate to the project root directory::

       cd dronetimeline

2. Run the application::

       python src/dtgui.py

3. Using the application:

   a. **Select Case Directory**: Use ``File > Select Case Directory`` to choose a folder for your case.
   b. **Import Timeline**: Use ``File > Import Timeline`` to import CSV timeline files.
   c. **Merge Timelines**: Use ``Timeline > Merge Timelines`` to combine imported timelines.
   d. **View Merged Timeline**: Use ``Timeline > Show Merged Timeline`` to view the merged result.

   If the Entity Recognition plugin is installed, entities will be automatically
   highlighted with yellow background in the merged timeline view.

Plugin Management
-----------------

To install a plugin::

    pip install --editable src/plugins/<PluginName>

To uninstall a plugin::

    pip uninstall <PluginName> -y

The application is modular — uninstalling a plugin simply removes that feature
without breaking the rest of the application.
