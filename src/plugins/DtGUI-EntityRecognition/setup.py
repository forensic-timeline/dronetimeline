from setuptools import setup, find_packages

setup(
    name="dronetimeline-DtGUI-EntityRecognition",
    version="1.0.0",
    description="DroneTimeline Entity Recognition Plugin - Rule-based forensic entity detection",
    long_description="Entity Recognition plugin for DroneTimeline, providing rule-based entity detection using spaCy to highlight forensic entities in merged timelines.",
    long_description_content_type="text/plain",
    author="Hudan Studiawan",
    author_email="hudan@if.its.ac.id",
    url="https://github.com/studiawan/dronetimeline",
    packages=find_packages(),
    package_data={
        "DtGUI_EntityRecognition": ["rules/*.jsonl"],
    },
    entry_points={
        "DtGUI": ["entityrecognition = DtGUI_EntityRecognition.plugin_hooks"],
    },
    install_requires=[
        "dronetimeline-DtGUI",
        "dronetimeline-QtDatabase",
        "spacy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
