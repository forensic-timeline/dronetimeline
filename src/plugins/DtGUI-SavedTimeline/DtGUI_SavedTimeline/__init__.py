# DtGUI Saved Timeline Plugin
from . import plugin_hooks
from . import saved_timeline

import pluggy

hookimpl = pluggy.HookimplMarker("DtGUI")
"""Marker to be imported and used in plugins (and for own implementations)"""
