import os
from setuptools import setup, find_packages

setup(
    name="apsbot",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "aps-toolkit",
        "pyperclip",
        "tabulate"
    ],
    entry_points={
        "console_scripts": [
            "apsbot=apsbot.cli:apsbot",
        ],
    },
    author="chuongmep",
    author_email="chuongpqvn@gmail.com",
    description="A simple CLI tool to interact with the Autodesk Forge API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chuongmep/aps-bot.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
