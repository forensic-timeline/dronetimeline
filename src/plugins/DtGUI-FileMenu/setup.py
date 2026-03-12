from setuptools import setup, find_packages

setup(
    name="dronetimeline-DtGUI-FileMenu",
    version="1.0.0",
    description="DroneTimeline File Menu Plugin - Select Directory, Import Timeline, Exit",
    long_description="File Menu plugin for DroneTimeline, providing case directory selection, CSV timeline import, and exit functionality.",
    long_description_content_type="text/plain",
    author="Hudan Studiawan",
    author_email="hudan@if.its.ac.id",
    url="https://github.com/studiawan/dronetimeline",
    packages=find_packages(),
    entry_points={
        "DtGUI": ["filemenu = DtGUI_FileMenu.plugin_hooks"],
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
