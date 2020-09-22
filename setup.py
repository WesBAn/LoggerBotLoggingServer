from setuptools import setup
from setuptools import find_packages

setup(
    name="LoggerBotLoggingServer",
    version="0.1",
    packages=find_packages(".", include=["bot_logging_server", "bot_logging_server.*"]),
    url="",
    license="LICENSE",
    author="mc-wesban",
    author_email="wesban1@gmail.com",
    description="",
    classifiers=[
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
