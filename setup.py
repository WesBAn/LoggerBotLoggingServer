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
)
