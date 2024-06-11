import os
from setuptools import setup, find_packages

setup(
    name="apsbot",
    version="0.2.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==8.1.3",
        "aps-toolkit",
        "pyperclip==1.8.2",
        "tabulate==0.9.0",
        "openai==1.33.0",
        "langchain-openai==0.1.8",
        "langchain_experimental==0.0.60",
        "langchain==0.2.3"
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
