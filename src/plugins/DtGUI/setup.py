from setuptools import setup, find_packages

setup(
    name="dronetimeline-DtGUI",
    version="1.0.0",
    description="DroneTimeline GUI - Core plugin host for forensic timeline analysis",
    long_description="DtGUI is the core GUI plugin for DroneTimeline, providing the main application window and plugin architecture using pluggy.",
    long_description_content_type="text/plain",
    author="Hudan Studiawan",
    author_email="hudan@if.its.ac.id",
    url="https://github.com/studiawan/dronetimeline",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["DtGUI = DtGUI.host:main"]
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