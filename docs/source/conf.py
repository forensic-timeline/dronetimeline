# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

project = 'DroneTimeline'
copyright = '2025, Muhammad Luthfi'
author = 'Muhammad Luthfi'
release = '1.0.0'

# Add plugin source directories to sys.path for autodoc
plugins_dir = os.path.abspath(os.path.join("..", "..", "src", "plugins"))
for plugin_name in os.listdir(plugins_dir):
    plugin_path = os.path.join(plugins_dir, plugin_name)
    if os.path.isdir(plugin_path):
        sys.path.insert(0, plugin_path)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'classic'
html_static_path = ['_static']
html_theme_options = {
    "sidebarwidth": "32%"
}
