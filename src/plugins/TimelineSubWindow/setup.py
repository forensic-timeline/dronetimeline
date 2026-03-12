from setuptools import setup, find_packages

setup(
    name="dronetimeline-TimelineSubWindow",
    version="1.0.0",
    description="DroneTimeline TimelineSubWindow - Timeline display plugin with HTML entity rendering",
    long_description="TimelineSubWindow plugin for DroneTimeline, providing the table view for displaying forensic timelines with HTML entity highlighting support.",
    long_description_content_type="text/plain",
    author="Hudan Studiawan",
    author_email="hudan@if.its.ac.id",
    url="https://github.com/studiawan/dronetimeline",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["TimelineSubWindow = TimelineSubWindow.host:main"]
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