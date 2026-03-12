from setuptools import setup, find_packages

setup(
    name="dronetimeline-DtGUI-SavedTimeline",
    version="1.0.0",
    description="DroneTimeline Saved Timeline Plugin - Quick access to previously imported timelines",
    long_description="Saved Timeline plugin for DroneTimeline, providing persistent storage and quick access to previously imported forensic timelines.",
    long_description_content_type="text/plain",
    author="Hudan Studiawan",
    author_email="hudan@if.its.ac.id",
    url="https://github.com/studiawan/dronetimeline",
    packages=find_packages(),
    entry_points={
        "DtGUI": ["savedtimeline = DtGUI_SavedTimeline.plugin_hooks"],
    },
    install_requires=[
        "dronetimeline-DtGUI",
        "dronetimeline-QtDatabase",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
