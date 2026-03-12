from setuptools import setup, find_packages

setup(
    name="dronetimeline-MergeTimelineSubWindow",
    version="1.0.0",
    description="DroneTimeline MergeTimelineSubWindow - Timeline merging plugin",
    long_description="MergeTimelineSubWindow plugin for DroneTimeline, providing UI for selecting and merging multiple forensic timelines.",
    long_description_content_type="text/plain",
    author="Hudan Studiawan",
    author_email="hudan@if.its.ac.id",
    url="https://github.com/studiawan/dronetimeline",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["MergeTimelineSubWindow = MergeTimelineSubWindow.host:main"]
    },
    install_requires=[
        "pluggy",
        "PyQt5"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)