from setuptools import setup, find_packages

setup(
    name="dronetimeline-DtGUI-TimelineMenu",
    version="1.0.0",
    description="DroneTimeline Timeline Menu Plugin - Merge Timelines, Show Merged Timeline",
    long_description="Timeline Menu plugin for DroneTimeline, providing timeline merging and merged timeline viewing functionality.",
    long_description_content_type="text/plain",
    author="Hudan Studiawan",
    author_email="hudan@if.its.ac.id",
    url="https://github.com/studiawan/dronetimeline",
    packages=find_packages(),
    entry_points={
        "DtGUI": ["timelinemenu = DtGUI_TimelineMenu.plugin_hooks"],
    },
    install_requires=[
        "dronetimeline-DtGUI",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
