import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fusexbox",
    version="0-dev",
    maintainer="Jannik Vogel",
    description="original Xbox remote filesystem driver based on FUSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JayFoxRox/fusexbox",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
    ),
    install_requires=[
        "fusepy",
        "xboxpy",
        "ioctl-opt",
    ],
    dependency_links=[
        "git+https://github.com/XboxDev/xboxpy.git#egg=xboxpy",
    ],
)
