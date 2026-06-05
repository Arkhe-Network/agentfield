#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="neuronal-communication-channels",
    version="1.0.0",
    description="Substrato 1069 — Neuronal Communication Channels",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20.0",
    ],
    python_requires=">=3.8",
)
