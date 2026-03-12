"""
Saved Timeline Manager

Handles reading and writing of saved timelines to a JSON file.
This allows users to quickly reopen previously imported timelines
without needing to reimport them.
"""

import os
import json
from typing import Dict, List, Any


class SavedTimelineManager:
    """
    Manages saved timelines stored in a JSON file.
    
    The JSON structure is:
    {
        "/path/to/case1": {
            "timelines": {
                "timeline1": ["col1", "col2", "col3"],
                "timeline2": ["colA", "colB"]
            }
        },
        "/path/to/case2": {...}
    }
    
    Attributes:
        json_path: Path to the JSON file storing timeline data
        timelines: In-memory cache of timeline data
    """

    def __init__(self, json_path: str = './timelines.json'):
        """
        Initialize the SavedTimelineManager.
        
        Args:
            json_path: Path to the JSON file. Defaults to './timelines.json'
        """
        self.json_path = json_path
        self.timelines = self._load_timelines()

    def _load_timelines(self) -> Dict[str, Any]:
        """
        Load saved timelines from the JSON file.
        
        Creates an empty file if it doesn't exist.
        
        Returns:
            Dictionary containing all saved timeline data
        """
        timelines = {}
        if os.path.isfile(self.json_path):
            with open(self.json_path, "r") as file:
                try:
                    timelines = json.load(file)
                except (json.JSONDecodeError, Exception):
                    timelines = {}
        else:
            # Create empty file
            with open(self.json_path, 'w+') as outfile:
                json.dump(timelines, outfile, indent=4)

        return timelines

    def save_timeline(self, case_directory: str, table_name: str, column_names: List[str]) -> None:
        """
        Save a timeline entry to the JSON file.
        
        If the timeline already exists, it will not be overwritten.
        
        Args:
            case_directory: Path to the case directory
            table_name: Name of the timeline table
            column_names: List of column names in the timeline
        """
        datas = self._load_timelines()

        if case_directory not in datas:
            datas[case_directory] = {}
        if 'timelines' not in datas[case_directory]:
            datas[case_directory]["timelines"] = {}

        # Only save if timeline doesn't already exist
        if table_name not in datas[case_directory]["timelines"]:
            datas[case_directory]["timelines"][table_name] = column_names

        with open(self.json_path, 'w') as outfile:
            json.dump(datas, outfile, indent=4)

        # Update in-memory cache
        self.timelines = datas

    def get_all_timelines(self) -> Dict[str, Any]:
        """
        Get all saved timelines.
        
        Returns:
            Dictionary containing all saved timeline data
        """
        return self.timelines
