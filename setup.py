import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="media-sanitizer-tmwalter98",
    version="0.0.1",
    author="Timothy Walter",
    author_email="email@timothywalter.dev",
    description="A tool for sanitizing and organizing movie and TV show \
                 collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tmwalter98/media_sanitizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)