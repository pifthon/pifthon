import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pifthon", # Replace with your own username
    version="0.1",
    author="Pifthon",
    author_email="pifthon@gmail.com",
    description="A information flow analyzer for Python programs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pifthon/pifthon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU AGPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
