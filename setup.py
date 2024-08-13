from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solapi-sms",
    version="0.1.0",
    author="RUNNERS",
    author_email="dev@runners.im",
    description="A Python library for sending SMS using SolApi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RUNNERS-IM/python-solapi-sms",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
    ],
)