How to build documentation
==========================

To build the documentation, follow these steps:

.. note:: Make sure Sphinx is installed: ``pip install sphinx``

1. Navigate to the documentation directory::

       cd docs

2. Clean up previously generated documentation::

       make clean

   On Windows::

       make.bat clean

3. Build the documentation::

       make html

   On Windows::

       make.bat html

4. Open the generated documentation.

   After building, find the HTML files in ``docs/build/html/``.
   Open ``index.html`` in your web browser to view the documentation.
